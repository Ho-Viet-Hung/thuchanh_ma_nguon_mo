import numpy as np
import matplotlib.pyplot as plt
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

def generate_random_data():
    x = np.linspace(0, 50, 50)
    y = np.linspace(0, 50, 50)

    x += np.random.uniform(-4, 4, 50)
    y += np.random.uniform(-4, 4, 50)
    return x, y

def plot_data(x, y):
    plt.scatter(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Training Data")
    plt.show()

def linear_regression(x, y, learning_rate, training_epochs):
    n = len(x)

    X = tf.placeholder("float")
    Y = tf.placeholder("float")
    W = tf.Variable(np.random.randn(), name="W")
    b = tf.Variable(np.random.randn(), name="b")

    y_pred = tf.add(tf.multiply(X, W), b)
    cost = tf.reduce_sum(tf.pow(y_pred - Y, 2)) / (2 * n)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)

        for epoch in range(training_epochs):
            for (_x, _y) in zip(x, y):
                sess.run(optimizer, feed_dict={X: _x, Y: _y})

            if (epoch + 1) % 50 == 0:
                c = sess.run(cost, feed_dict={X: x, Y: y})
                print("Epoch", (epoch + 1), ": cost =", c, "W =", sess.run(W), "b =", sess.run(b))

        training_cost = sess.run(cost, feed_dict={X: x, Y: y})
        weight = sess.run(W)
        bias = sess.run(b)

    return weight, bias, training_cost

def plot_regression_line(x, y, weight, bias):
    predictions = weight * x + bias
    plt.plot(x, y, 'ro', label='Original data')
    plt.plot(x, predictions, label='Fitted line')
    plt.title('Linear Regression Result')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    x, y = generate_random_data()
    plot_data(x, y)

    learning_rate = 0.01
    training_epochs = 1000

    weight, bias, training_cost = linear_regression(x, y, learning_rate, training_epochs)

    print("Training cost =", training_cost, "Weight =", weight, "bias =", bias, '\n')

    plot_regression_line(x, y, weight, bias)
