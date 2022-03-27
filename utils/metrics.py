from skimage.metrics import hausdorff_distance as hd
import numpy as np

def hd_land(target, pred, shape):
    set_ax = target[:,0].tolist()
    set_ay = target[:,1].tolist()

    set_bx = pred[:,0].tolist() 
    set_by = pred[:,1].tolist() 

    coords_a = np.zeros(shape, dtype=bool)
    coords_b = np.zeros(shape, dtype=bool)
    for x, y in zip(set_ax, set_ay):
        coords_a[(x, y)] = True

    for x, y in zip(set_bx, set_by):
        coords_b[(x, y)] = True
    
    dist = hd(coords_a, coords_b)
    
    return dist
    
def hd_landmarks(out, label, size = 1024, heart = False):
    shape = (size, size)

    target = np.round(label.cpu().numpy()*size).astype('int32').clip(0, size - 1)
    pred = np.round(out.cpu().numpy()*size).astype('int32').clip(0, size - 1)
    
    hd_RL = hd_land(target[:44,:], pred[:44,:], shape)
    hd_LL = hd_land(target[44:94,:], pred[44:94,:], shape)
    
    if heart:
        hd_H = hd_land(target[94:120,:], pred[94:120,:], shape)
        return hd_RL, hd_LL, hd_H
    else:
        return hd_RL, hd_LL
