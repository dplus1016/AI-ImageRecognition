# Teachable Machine 사이트에서 복사한 코드
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

def judge(f_name,m_name,l_name):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    path='/content/drive/My Drive/model/'
    model = tensorflow.keras.models.load_model(m_name,compile=False)
    
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    # Replace this with the path to your image
    image = Image.open(f_name)
    
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    
    #n the image into a numpy array
    image_array = np.asarray(image)
    
    # display the resized image
    image.show()
    
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    
    # Load the image into the array
    data[0] = normalized_image_array
    
    # run the inference
    prediction = model.predict(data)
    print(prediction)
    
    #사용자 추가
    # 가장 큰 값의 인덱스 찾기
    prediction = prediction[0]
    max_v=prediction[0]
    max_i=0
    for i in range(len(prediction)):
        if max_v<prediction[i]:
            max_v=prediction[i]
            max_i=i
    
    print(max_i)

    # label 파일 참조하기
    with open(l_name,'r',encoding='UTF8') as f:
        label=f.readlines()
        print(label[max_i][2:-1],": %d%%" % (max_v*100))

    return(label[max_i][2:-1] + "("+ str(round(max_v*100,2))+"%)")
