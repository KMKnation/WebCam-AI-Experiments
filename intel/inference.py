import argparse
import time
import cv2
import imutils
import os
import config
import numpy as np
from intel.network import Network
from imutils.video import FPS

'source /opt/intel/openvino/bin/setupvars.sh -pyver 3.5'

CPU_EXTENSION = "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so"
cascade = cv2.CascadeClassifier(config.CASCADE_PATH)


def pre_process(frame, net_input_shape):
    p_frame = cv2.resize(frame, (net_input_shape[3], net_input_shape[2]))
    p_frame = p_frame.transpose(2, 0, 1)
    # p_frame = np.expand_dims(p_frame, axis=1)
    p_frame = p_frame.reshape(1, *p_frame.shape)
    return p_frame

def get_faces(frame):
    faces = cascade.detectMultiScale(frame,
                                     scaleFactor=1.1,
                                     minNeighbors=3)
    if len(faces) >= 1:
        return faces
    else:
        return []


def process_on_face(face, frame):
    x = face[0] - 20
    y = face[1] - 20
    w = face[2] + 20
    h = face[3] + 20

    face_frame = frame[y: y + h, x:x + w]
    # cv2.imshow('face', face_frame)
    # cv2.waitKey(0)

    return face_frame, face
    # return pre_process()

from datetime import datetime
def infer_on_video(args):
    plugin = Network()
    emotion_plugin = Network()
    # load the model
    plugin.load_model(args.m, args.d, CPU_EXTENSION)
    emotion_plugin.load_model(args.em, args.d, CPU_EXTENSION)
    print('Model Loaded !!!')


    emo_labels = ['neutral', 'happy', 'sad', 'surprise', 'anger']

    net_input_shape = plugin.get_input_shape()
    net_emo_input_shape = emotion_plugin.get_input_shape()

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(args.o, fourcc, 20.0, (100, 100))

    cap = cv2.VideoCapture(args.i)
    fps = FPS().start()

    counter = 0
    # Capture frame-by-frame
    lasttime = datetime.now()
    last_second = -1
    while (cap.isOpened()):
        isPending, frame = cap.read()


        if not isPending:
            break

        diff_time = datetime.now() - lasttime
        if (diff_time.seconds > last_second):  # process frame on each one second
            last_second = diff_time.seconds
            # print(diff_time.seconds)

        try:
            faces = get_faces(frame)
            if (len(faces) > 0):
                for face in faces:
                    p_frame, face = process_on_face(face, frame)
                    face_frame = pre_process(p_frame, net_input_shape)
                    emo_frame = pre_process(p_frame, net_emo_input_shape)

                    cv2.rectangle(frame, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (0, 255, 0), 2)


                    # p_frame = pre_process(frame, net_input_shape)
                    # time.sleep(0.03)
                    # k = cv2.waitKey(30)
                    # Perform inference on the frame
                    plugin.async_inference(face_frame)
                    emotion_plugin.async_inference(emo_frame)

                    if(emotion_plugin.wait() == 0):
                        result = emotion_plugin.extract_all_output()
                        em_index = np.argmax(result['prob_emotion'][0])
                        em_proba = result['prob_emotion'][0][em_index][0][0] * 100
                        emo_pred = str(emo_labels[em_index])+ ':' +str(em_proba)
                        cv2.putText(frame, emo_pred[:10], (face[0], face[1] + face[3] + 25), config.font,
                                    config.fontScale, config.emocolor, config.thickness, cv2.LINE_AA)

                    # Get the output of inference
                    if plugin.wait() == 0:
                        result = plugin.extract_all_output()
                        age = result['age_conv3'][0][0][0][0] * 100
                        gender = ''
                        if result['prob'][0][1][0][0] > result['prob'][0][0][0][0]:
                            gender = 'Male ' + str(result['prob'][0][1][0][0] * 100)
                        else:
                            gender = 'Female ' + str(result['prob'][0][0][0][0] * 100)

                        ans = "Age :" + str(age)[:5] + " & G:" + gender[:10]
                        cv2.putText(frame, ans, (face[0], face[1]), config.font,
                                    config.fontScale, config.color, config.thickness, cv2.LINE_AA)
                        fps.update()


        except Exception as err:
            print(err)

        cv2.imshow('output', imutils.resize(frame, width=700))

        ### TODO: Write out the frame, depending on image or video
        if (args.o.split('.')[1] == 'avi'):
            out.write(frame)
        # else:
        #     cv2.imwrite(args.o, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    ### TODO: Close the stream and any windows at the end of the application
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    out.release()


def get_args():
    '''
    Gets the arguments from the command line.
    '''
    parser = argparse.ArgumentParser("Run inference on an input video")
    # -- Create the descriptions for the commands
    m_desc = "The location of the model XML file"
    i_desc = "The location of the input file"
    d_desc = "The device name, if not 'CPU'"

    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # -- Create the arguments
    required.add_argument("-m", help=m_desc, required=False)
    optional.add_argument("-i", help=i_desc, default='')
    optional.add_argument("-d", help=d_desc, default='CPU')
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    args.i = '/home/hb/Videos/148796169.webm'
    args.m = '/home/hb/machinelearning/intel/models/intel/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml'
    args.em = '/home/hb/machinelearning/intel/models/intel/emotions-recognition-retail-0003/FP32/emotions-recognition-retail-0003.xml'
    args.o = 'out.avi'
    infer_on_video(args)


if __name__ == "__main__":
    main()

# If
