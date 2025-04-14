import numpy as np
import cv2 as cv
import imageio

# ----- Input video and calibration parameters -----
video_file = 'media/checkerboard_1x.mp4'
K = np.array([[1.11627287e+03, 0.00000000e+00, 6.41543816e+02],
              [0.00000000e+00, 1.11660375e+03, 3.45253748e+02],
              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist_coeff = np.array([1.91785858e-01, -8.45329913e-01, -3.28389992e-03, 1.33403506e-03, 1.40372357e+00])
board_pattern = (10, 7)
board_cellsize = 0.02
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

# ----- Open the video -----
video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

# Prepare 3D chessboard object points
obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# ----- Load and resize the nyan cat GIF to 1/4 size -----
nyan_frames = imageio.mimread('media/nyan.gif')
converted_frames = []
for frame in nyan_frames:
    if frame.shape[2] == 4:
        frame_bgra = cv.cvtColor(frame, cv.COLOR_RGBA2BGRA)
    else:
        frame_bgra = cv.cvtColor(frame, cv.COLOR_RGB2BGRA)
    # Resize to 1/4 using separate interpolation for alpha
    h, w = frame_bgra.shape[:2]
    new_w, new_h = w // 4, h // 4
    if new_w == 0 or new_h == 0:
        new_w, new_h = 1, 1  # Ensure at least 1x1 size
    # Resize color and alpha channels
    color = cv.resize(frame_bgra[:, :, :3], (new_w, new_h), interpolation=cv.INTER_AREA)
    alpha = cv.resize(frame_bgra[:, :, 3], (new_w, new_h), interpolation=cv.INTER_NEAREST)
    # Merge back
    resized_frame = cv.merge([color[:, :, 0], color[:, :, 1], color[:, :, 2], alpha])
    converted_frames.append(resized_frame)
nyan_frames = converted_frames
gif_frame_count = len(nyan_frames)
gif_index = 0

# ----- Setup the VideoWriter -----
fps = video.get(cv.CAP_PROP_FPS)
frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))

# ----- Helper function to overlay with perspective -----
def overlay_perspective(img, gif_frame, obj_pts, rvec, tvec, K, dist_coeff):
    """ Overlay GIF onto the image using perspective transformation based on 3D points """
    # Project 3D points to 2D
    img_pts, _ = cv.projectPoints(obj_pts, rvec, tvec, K, dist_coeff)
    img_pts = img_pts.reshape(-1, 2).astype(np.float32)
    # Source points (GIF corners)
    h, w = gif_frame.shape[:2]
    src_pts = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
    # Compute homography
    H, _ = cv.findHomography(src_pts, img_pts)
    if H is None:
        return img
    # Warp GIF
    warped = cv.warpPerspective(gif_frame, H, (img.shape[1], img.shape[0]), borderMode=cv.BORDER_TRANSPARENT)
    # Blend using alpha channel
    alpha = warped[:, :, 3] / 255.0
    overlay_img = warped[:, :, :3]
    # Blend
    img = (overlay_img * alpha[:, :, np.newaxis] + img * (1 - alpha[:, :, np.newaxis])).astype(np.uint8)
    return img

# ----- Main processing loop -----
while True:
    valid, img = video.read()
    if not valid:
        break

    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    
    if success:
        # Refine corners
        img_points = cv.cornerSubPix(cv.cvtColor(img, cv.COLOR_BGR2GRAY), img_points, (11,11), (-1,-1), 
                                    (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01))
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)
        
        # Define 3D points for GIF on X-Z plane (Y=0)
        gif_size = board_cellsize * 2  # Adjust size as needed
        
        obj_pts_gif = np.array([
            [-gif_size/2, 0, -gif_size/2],
            [gif_size/2, 0, -gif_size/2],
            [gif_size/2, 0, gif_size/2],
            [-gif_size/2, 0, gif_size/2]
        ], dtype=np.float32)
        
        # Overlay with perspective
        img = overlay_perspective(img, nyan_frames[gif_index], obj_pts_gif, rvec, tvec, K, dist_coeff)
        
        # Optional: Display camera position
        R, _ = cv.Rodrigues(rvec)
        p = (-R.T @ tvec).flatten()
        info = f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]'
        cv.putText(img, info, (10, 100), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
    
    # Display and save
    cv.imshow('Pose Estimation with Nyan Cat', img)
    out.write(img)
    
    gif_index = (gif_index + 1) % gif_frame_count

    key = cv.waitKey(10)
    if key == ord(' '):
        key = cv.waitKey()
    if key == 27:
        break

# ----- Release resources -----
video.release()
out.release()
cv.destroyAllWindows()