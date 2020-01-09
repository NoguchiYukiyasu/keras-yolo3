# -*- coding: utf-8 -*-
import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image
import glob 
import os

images_folder = "test_images"
result_folder = "result_folder"

def detect_images(yolo,images_folder,result_folder):
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    print("windowsでやってね")
    image_names = glob.glob("./"+images_folder+"/*.jPg") + glob.glob("./"+images_folder+"/*.jPeg") # windows
    for image_name in image_names:
        image = Image.open(image_name)
        r_image,bndboxs = yolo.detect_image_for_metrics(image)
        class_names = bndboxs["class_list"]
        score_list = bndboxs["score_list"]
        left_list = bndboxs["left_list"]
        top_list = bndboxs["top_list"]
        right_list = bndboxs["right_list"]
        bottom_list = bndboxs["bottom_list"]
        
        r_image.show()


        name,ext = os.path.splitext(os.path.basename(image_name))
        with open(result_folder+"/"+name+".txt", mode='w') as f:
            for i in range(len(class_names)):
                width = right_list[i]-left_list[i]
                height = bottom_list[i] - top_list[i]
                # print(class_names[i])
                f.write(class_names[i]+" "+str(score_list[i])+" "+str(left_list[i])+" "+str(top_list[i])+" "+str(width)+" "+str(height)+"\n") # <class_name> <confidence> <left> <top> <width> <height>
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors_path', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()
    detect_images(YOLO(**vars(FLAGS)),images_folder,result_folder)
    """
    if FLAGS.image:
    #Image detection mode, disregard any remaining command line arguments
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
    """