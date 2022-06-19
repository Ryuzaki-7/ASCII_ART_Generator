import cv2
import shutil
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont

# Characters used for Mapping to Pixels
Character = {
    "standard": "@%#*+=-:. ",
    "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}


def get_data(mode):
    font = ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=20)
    scale = 2
    char_list = Character[mode]
    return char_list, font, scale

#input from user
user_input = input("Enter the path of your file: ")


# Making Background Black or White
col = input("Select bg color(w/b): ")
bg = col
if bg == "w":
    bg_code = (255,255,255)
elif bg == "b":
    bg_code = (0,0,0)

# Getting the character List, Font and Scaling characters for square Pixels
char_list, font, scale = get_data("complex")
num_chars = len(char_list)
num_cols = 300


#--------------------------------------------Function to convert Video into ASCII Art-----------------------------------------------------

def v2a(user_input):
    
    cwd  = os.getcwd()
    dir = os.path.join(cwd,"Video_to_Photo")
    if not os.path.exists(dir):
        os.mkdir(dir)
    def convert_frames_to_video(input_list,output_file_name,fps,size):
        
        # Define the output video writer object 
        out = cv2.VideoWriter(output_file_name, fourcc, fps, size)
        num_frames = len(input_list)

        for i in range(num_frames):
            base_name='frame'
            img_name = base_name + '{:1d}'.format(i) + '.jpg'
            img_path = os.path.join(input_frame_path,img_name)
            print(img_path)
        
            img = cv2.imread(img_path)
            out.write(img)
            
        out.release()
        print("The output video is {} is saved in {}".format(output_file_name,cwd))
    
    
    vid = cv2.VideoCapture(user_input)
    currentframe = 0
    success, frame = vid.read()
    if success:
        # continue creating images until video remains
        name = './Video_to_Photo/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)

        # writing the extracted images
        cv2.imwrite(name, frame)
        
        # Reading Input Image
        image = cv2.imread('./Video_to_Photo/frame'+str(currentframe)+ '.jpg')
        
        # Extracting height and width from Image
        height, width, _ = image.shape

        # Defining height and width of each cell==pixel
        cell_w = width / num_cols
        cell_h = scale * cell_w
        num_rows = int(height / cell_h)

        # Calculating Height and Width of the output Image
        char_width, char_height = font.getsize("A")
        out_width = char_width * num_cols
        out_height = scale * char_height * num_rows

        # Making a new Image using PIL
        out_image = Image.new("RGB", (out_width, out_height), bg_code)
        draw = ImageDraw.Draw(out_image)

        #mapping characters for rgb
        for i in range(num_rows):
            for j in range(num_cols):
                partial_image = image[int(i*cell_h):min(int((i+1)*cell_h),height),
                                    int(j*cell_w):min(int((j+1)*cell_w),width), :]
                partial_avg_color = np.sum(np.sum(partial_image,axis=0),axis=0)/(cell_h*cell_w)
                partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
                c = char_list[min(int(np.mean(partial_image)*num_chars/255),num_chars-1)]
                draw.text((j*char_width,i*char_height), c, fill = partial_avg_color, font = font)

        # Inverting Image and removing excess borders
        if bg == "w":
            cropped_image = ImageOps.invert(out_image).getbbox()
        elif bg == "b":
            cropped_image = out_image.getbbox()

        # Saving the new Image
        out_image = out_image.crop(cropped_image)
        out_image.save('./Video_to_Photo/frame' + str(currentframe) + '.jpg')

        currentframe += 1


    while(True):
        success, frame = vid.read()
        if success:
            # continue creating images until video remains
            name = './Video_to_Photo/frame' + str(currentframe) + '.jpg'
            print('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)
        
            # Reading Input Image
            image = cv2.imread('./Video_to_Photo/frame'+str(currentframe)+ '.jpg')

            # Making a new Image using PIL
            out_image = Image.new("RGB", (out_width, out_height), bg_code)
            draw = ImageDraw.Draw(out_image)

            #mapping characters for rgb
            for i in range(num_rows): 
                for j in range(num_cols):
                    partial_image = image[int(i*cell_h):min(int((i+1)*cell_h),height),
                                        int(j*cell_w):min(int((j+1)*cell_w),width), :]
                    partial_avg_color = np.sum(np.sum(partial_image,axis=0),axis=0)/(cell_h*cell_w)
                    partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
                    c = char_list[min(int(np.mean(partial_image)*num_chars/255),num_chars-1)]
                    draw.text((j*char_width,i*char_height), c, fill = partial_avg_color, font = font)

            # Inverting Image and removing excess borders
            if bg == "white":
                cropped_image = ImageOps.invert(out_image).getbbox()
            elif bg == "black":
                cropped_image = out_image.getbbox()

            # Saving the new Image
            out_image = out_image.crop(cropped_image)
            out_image.save('./Video_to_Photo/frame' + str(currentframe) + '.jpg')
        
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    vid.release()
    cv2.destroyAllWindows()

    if __name__=='__main__':
        #PATH
        input_frame_path = "./Video_to_Photo/"
        img_list = os.listdir(input_frame_path)
        frame = cv2.imread(os.path.join(input_frame_path,'frame0.jpg'))
        height, width, channels = frame.shape
        fps = 20
        output_file_name = 'ascii.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        size = (width,height)
        convert_frames_to_video(img_list,output_file_name,fps,size)
        
    shutil.rmtree(dir)


#------------------------------------------------Function to Convert Picture to ASCII art------------------------------------------------------  

def p2a(user_input):
    # Reading Input Image
    image = cv2.imread(user_input)

    # Extracting height and width from Image
    height, width, _ = image.shape

    # Defining height and width of each cell==pixel
    cell_w = width / num_cols
    cell_h = scale * cell_w
    num_rows = int(height / cell_h)

    # Calculating Height and Width of the output Image
    char_width, char_height = font.getsize("A")
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows

    # Making a new Image using PIL
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    #mapping characters for rgb
    for i in range(num_rows):
        for j in range(num_cols):
            partial_image = image[int(i*cell_h):min(int((i+1)*cell_h),height),
                                int(j*cell_w):min(int((j+1)*cell_w),width), :]
            partial_avg_color = np.sum(np.sum(partial_image,axis=0),axis=0)/(cell_h*cell_w)
            partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
            c = char_list[min(int(np.mean(partial_image)*num_chars/255),num_chars-1)]
            draw.text((j*char_width,i*char_height), c, fill = partial_avg_color, font = font)

    # Inverting Image and removing excess borders
    if bg == "w":
        cropped_image = ImageOps.invert(out_image).getbbox()
    elif bg == "b":
        cropped_image = out_image.getbbox()

    # Saving the new Image
    out_image = out_image.crop(cropped_image)
    out_image.save("./output.jpg")
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

if user_input.endswith('.jpg'):
    p2a(user_input)
elif user_input.endswith('.mp4'):
    v2a(user_input)
else:
    print("Format not supported")
