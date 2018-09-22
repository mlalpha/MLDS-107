import numpy as np

from keras.models import Sequential
from keras.layers import Dense,Activation

def generate_data_1():
    x = np.linspace(0.00001,1,9999)
    y = np.sin(5*np.pi*x)/(5*np.pi*x)

    index=list(range(0,9999))
    np.random.seed(1024)
    np.random.shuffle(index)

    x_u = x[index]
    y_u = y[index]

    x_train = x_u[0:9000]
    y_train = y_u[0:9000]

    x_test = x_u[9000:]
    y_test = y_u[9000:]
    return (x_train,y_train,x_test,y_test,x,y)
  
def generate_data_2():
    x = np.linspace(0.00001,1,9999)
    y = np.sign( np.sin(5*np.pi*x) )

    index=list(range(0,9999))
    np.random.seed(1024)
    np.random.shuffle(index)

    x_u = x[index]
    y_u = y[index]

    x_train = x_u[0:9000]
    y_train = y_u[0:9000]

    x_test = x_u[9000:]
    y_test = y_u[9000:]
    return (x_train,y_train,x_test,y_test,x,y)

def model_generator_1():
    print('model_1 build')
    model = Sequential()
    model.add( Dense( 5 , input_shape=(1,) ) )
    model.add( Activation('relu') ) 

    model.add( Dense(5) )
    model.add( Activation('relu') ) 

    model.add( Dense(5) )
    model.add( Activation('relu') ) 

    model.add( Dense(5) )
    model.add( Activation('relu') ) 
    
    model.add( Dense(5) )
    model.add( Activation('relu') ) 
    
    model.add( Dense(1) )
    model.compile( loss = 'mse', optimizer='adam')
    print(model.summary())
    return model
  
def model_generator_2():
    print('model_3 build')
    model = Sequential()
    model.add( Dense( 10 , input_shape=(1,) ) )
    model.add( Activation('relu') ) 

    model.add( Dense(6) )
    model.add( Activation('relu') ) 
    
    model.add( Dense(6) )
    model.add( Activation('relu') ) 
    
    model.add( Dense(1) )
    model.compile( loss = 'mse', optimizer='adam')
    print(model.summary())
    return model  
  
def model_generator_3():
    print('model_2 build')
    model = Sequential()
    model.add( Dense( 45 , input_shape=(1,) ) )
    model.add( Activation('relu') ) 
    
    model.add( Dense(1) )
    model.compile( loss = 'mse', optimizer='adam')
    print(model.summary())
    return model


    
import matplotlib.pyplot as plt          

def train(x_train,y_train,x_test,y_test,x,y,epochs):
    
    model_1 = model_generator_1()
    model_2 = model_generator_2()
    model_3 = model_generator_3()
    
    history_1 = model_1.fit( x_train, y_train, batch_size=100, epochs=epochs, verbose=1, validation_data=(x_test,y_test) )
    history_2 = model_2.fit( x_train, y_train, batch_size=100, epochs=epochs, verbose=1, validation_data=(x_test,y_test) )
    history_3 = model_3.fit( x_train, y_train, batch_size=100, epochs=epochs, verbose=1, validation_data=(x_test,y_test) )
    
    
    plt.plot(history_1.history['val_loss'], color = 'blue')
    plt.plot(history_2.history['val_loss'], color = 'brown')
    plt.plot(history_3.history['val_loss'], color = 'green')
    
    plt.show()
    
    y_1 = model_1.predict(x)
    y_2 = model_2.predict(x)
    y_3 = model_3.predict(x)
    
    plt.plot(y)
    plt.plot(y_1, color = 'blue')
    plt.plot(y_2, color = 'brown')
    plt.plot(y_3, color = 'green')
    
    plt.show()
    
    
def main():   
    x_train,y_train,x_test,y_test,x,y = generate_data_1()
    train(x_train,y_train,x_test,y_test,x,y,50)
    x_train,y_train,x_test,y_test,x,y = generate_data_2()
    train(x_train,y_train,x_test,y_test,x,y,150)
    
if __name__ == '__main__':
    main()