import torch as T
import torch.nn.functional as F
import numpy as np

from neuralnet_pytorch import utils

__all__ = ['huber_loss', 'first_derivative_loss', 'lp_loss', 'ssim', 'psnr', 'chamfer_loss', 'iou_loss']


def huber_loss(x, y, reduction='mean'):
    return F.smooth_l1_loss(x, y, reduction)


def first_derivative_loss(x, y, p=2):
    if x.ndimension() != 4 and y.ndimension() != 4:
        raise TypeError('y and y_pred should have four dimensions')
    kern_x = T.from_numpy(np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype='float32')).requires_grad_(False)
    kern_x = T.flip(kern_x.expand(y.shape[1], y.shape[1], 3, 3), (0, 1))

    kern_y = T.from_numpy(np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype='float32')).requires_grad_(False)
    kern_y = T.flip(kern_y.expand(y.shape[1], y.shape[1], 3, 3), (0, 1))

    if utils.cuda_available:
        kern_x = kern_x.cuda()
        kern_y = kern_y.cuda()

    x_grad_x = F.conv2d(x, kern_x, padding=1)
    x_grad_y = F.conv2d(x, kern_y, padding=1)
    x_grad = T.sqrt(x_grad_x ** 2 + x_grad_y ** 2 + 1e-10)

    y_grad_x = F.conv2d(y, kern_x, padding=1)
    y_grad_y = F.conv2d(y, kern_y, padding=1)
    y_grad = T.sqrt(y_grad_x ** 2 + y_grad_y ** 2 + 1e-10)
    return lp_loss(x_grad, y_grad, p)


def lp_loss(x, y, p=2, reduction='mean'):
    """
    Calculates p-norm of (x - y)

    :param x: a Torch.tensor
    :param y: a Torch.tensor of the same shape as x
    :param p: order of the norm
    :param reduction: 'mean' or 'sum'
    :return: the p-norm of (x - y)
    """
    if y.ndimension() != x.ndimension():
        raise TypeError('y should have the same shape as y_pred', ('y', y.data.type(), 'y_pred', x.data.type()))

    if p == 1:
        return F.l1_loss(x, y, reduction=reduction)
    elif p == 2:
        return F.mse_loss(x, y, reduction=reduction)
    else:
        return T.mean(T.abs(x - y) ** p)


def iou_loss(x, y):
    """
    Adapted from https://github.com/345ishaan/DenseLidarNet/blob/master/code/iou_loss.py

    :param x: an image of size (b, c, h, w)
    :param y: an image of the same shape as x
    :return: the intersection over union score
    """
    def compute_intersection(preds, gts):
        corner_preds_low, _ = T.min(preds, 1.)
        corner_preds_high, _ = T.max(preds, 1.)

        corner_gts_low, _ = T.min(gts, 1.)
        corner_gts_high, _ = T.max(gts, 1.)

        corner_low, _ = T.max(T.stack([corner_preds_low, corner_gts_low]), 0.)
        corner_high, _ = T.min(T.stack([corner_preds_high, corner_gts_high]), 0.)

        corner_preds_diff = corner_preds_high - corner_preds_low
        corner_gts_diff = corner_gts_high - corner_gts_low

        area_preds = T.prod(corner_preds_diff, 1.)
        area_gts = T.prod(corner_gts_diff, 1.)
        return corner_low, corner_high, area_preds, area_gts

    corner_low, corner_high, area_preds, area_gts = compute_intersection(x, y)
    corner_diff = corner_high - corner_low
    intersection = T.prod(corner_diff, 1.)
    union = area_gts + area_preds - intersection
    iou = intersection / (union + 1e-8)
    return iou


def chamfer_loss(xyz1, xyz2, reduce='sum', c_code=False):
    """
    The Pytorch code is adapted from https://github.com/345ishaan/DenseLidarNet/blob/master/code/chamfer_loss.py
    The CUDA code is adapted from https://github.com/ThibaultGROUEIX/AtlasNet/tree/master/extension

    :param xyz1: a point cloud of shape (b, n1, 3)
    :param xyz2: a point cloud of shape (b, n2, 3)
    :param reduce: 'mean' or 'sum'. Default is 'sum'
    :param c_code: whether to use CUDA implementation. This version is much more memory-friendly and slightly faster
    :return: the Chamfer distance between the two point clouds
    """
    assert reduce in ('mean', 'sum'), 'Unknown reduce method'

    def batch_pairwise_dist(x, y):
        bs, num_points_x, points_dim = x.size()
        _, num_points_y, _ = y.size()
        xx = T.bmm(x, x.transpose(2, 1))
        yy = T.bmm(y, y.transpose(2, 1))
        zz = T.bmm(x, y.transpose(2, 1))

        if utils.cuda_available:
            dtype = T.cuda.LongTensor
        else:
            dtype = T.LongTensor

        diag_ind_x = T.arange(0, num_points_x).type(dtype)
        diag_ind_y = T.arange(0, num_points_y).type(dtype)
        # brk()
        rx = xx[:, diag_ind_x, diag_ind_x].unsqueeze(1).expand_as(zz.transpose(2, 1))
        ry = yy[:, diag_ind_y, diag_ind_y].unsqueeze(1).expand_as(zz)
        P = (rx.transpose(2, 1) + ry - 2 * zz)
        return P

    if c_code:
        from .extensions import chamfer_distance
        dist1, dist2 = chamfer_distance(xyz1, xyz2)
    else:
        P = batch_pairwise_dist(xyz1, xyz2)
        dist2, _ = T.min(P, 1)
        dist1, _ = T.min(P, 2)
    loss_2 = T.sum(dist2)
    loss_1 = T.sum(dist1)
    return (T.mean(loss_1) + T.mean(loss_2)) if reduce == 'mean' else (T.sum(loss_1) + T.sum(loss_2))


def _fspecial_gauss(size, sigma):
    """Function to mimic the 'fspecial' gaussian MATLAB function
    """
    x, y = np.mgrid[-size // 2 + 1:size // 2 + 1, -size // 2 + 1:size // 2 + 1]
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2)))
    return g / np.sum(g)


def ssim(img1, img2, max_val=1., filter_size=11, filter_sigma=1.5, k1=0.01, k2=0.03, cs_map=False):
    """Return the Structural Similarity Map between `img1` and `img2`.
    This function attempts to match the functionality of ssim_index_new.m by
    Zhou Wang: http://www.cns.nyu.edu/~lcv/ssim/msssim.zip
    Arguments:
    img1: Numpy array holding the first RGB image batch.
    img2: Numpy array holding the second RGB image batch.
    max_val: the dynamic range of the images (i.e., the difference between the
      maximum the and minimum allowed values).
    filter_size: Size of blur kernel to use (will be reduced for small images).
    filter_sigma: Standard deviation for Gaussian blur kernel (will be reduced
      for small images).
    k1: Constant used to maintain stability in the SSIM calculation (0.01 in
      the original paper).
    k2: Constant used to maintain stability in the SSIM calculation (0.03 in
      the original paper).
    Returns:
    Pair containing the mean SSIM and contrast sensitivity between `img1` and
    `img2`.
    Raises:
    RuntimeError: If input images don't have the same shape or don't have four
      dimensions: [batch_size, height, width, depth].
    """
    if img1.ndimension() != 4:
        raise RuntimeError('Input images must have four dimensions, not %d', img1.ndimension())

    _, _, height, width = img1.shape

    # Filter size can't be larger than height or width of images.
    size = min((filter_size, height, width))

    # Scale down sigma if a smaller filter size is used.
    sigma = (size * filter_sigma / filter_size) if filter_size else 1.

    if filter_size:
        window = T.flip(T.tensor(_fspecial_gauss(size, sigma)), (0, 1)).view(1, 1, size, size).type(
            T.float32).requires_grad_(False)
        if utils.cuda_available:
            window = window.cuda()

        mu1 = F.conv2d(img1, window)
        mu2 = F.conv2d(img2, window)
        sigma11 = F.conv2d(img1 * img1, window)
        sigma22 = F.conv2d(img2 * img2, window)
        sigma12 = F.conv2d(img1 * img2, window)
    else:
        # Empty blur kernel so no need to convolve.
        mu1, mu2 = img1, img2
        sigma11 = img1 * img1
        sigma22 = img2 * img2
        sigma12 = img1 * img2

    mu1 = mu1 * mu1
    mu2 = mu2 * mu2
    mu12 = mu1 * mu2
    sigma11 -= mu1
    sigma22 -= mu2
    sigma12 -= mu12

    # Calculate intermediate values used by both ssim and cs_map.
    c1 = (k1 * max_val) ** 2
    c2 = (k2 * max_val) ** 2
    v1 = 2.0 * sigma12 + c2
    v2 = sigma11 + sigma22 + c2
    ssim = T.mean((((2.0 * mu12 + c1) * v1) / ((mu1 + mu2 + c1) * v2 + 1e-10)))
    output = ssim if not cs_map else (ssim, T.mean(v1 / v2))
    return output


def psnr(x, y):
    """PSNR for [0,1] images"""
    return -10 * T.log(T.mean((y - x) ** 2)) / np.log(10.)
