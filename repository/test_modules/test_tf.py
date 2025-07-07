from artiq.experiment import *
import tensorflow as tf



class TestTF(EnvExperiment):
    def build(self):
        self.setattr_device("core")
    
    @rpc
    def tf(self) -> TList:
        # 1. Load the dataset
        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        # Normalize the data
        x_train, x_test = x_train / 255.0, x_test / 255.0

        # 2. Build the model
        model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
        ])

        # 3. Compile the model
        model.compile(optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])

        # 4. Train the model
        model.fit(x_train, y_train, epochs=5)

        # 5. Evaluate the model
        print("\nEvaluating the model on the test data:")
        return TList(model.evaluate(x_test,  y_test, verbose=2))

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()


        print(tf.__version__)
        print(self.tf)


        