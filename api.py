import flask
from flask import Flask, render_template, request,make_response
import joblib
#from sklearn.externals import joblib
import inputScript
import regex
import mysql.connector
from mysql.connector import Error
import random
import sys
import socket
import logging
import smtplib 
import json  #json request
import ssl, socket
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix,classification_report
#from sklearn.metrics import confusionmatrix
import confusionmatrix
import seaborn as sn
from sklearn.metrics import beautifulsoup
#import beautifulsoup
import email, smtplib, ssl
from sklearn import metrics

import numpy as np 
import seaborn as sn 
import matplotlib.pyplot as plt 

loggeduser='kavanaravi1@gmail.com'


app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

def  rnn():
        
    nltk.download('punkt')

    def preprocess_text(text):        
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text.lower()

   
    labels = [1] * len(malicious_urls) + [0] * len(benign_urls)

    
    all_urls = malicious_urls + benign_urls
    all_urls = [preprocess_text(url) for url in all_urls]

    
    X_train, X_test, y_train, y_test = train_test_split(all_urls, labels, test_size=0.2, random_state=42)

  
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    
    classifier = MultinomialNB()
    classifier.fit(X_train_vec, y_train)

   
    y_pred = classifier.predict(X_test_vec)

    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:\n", classification_report(y_test, y_pred))

   
    sample_input = ["newmaliciousurl.com", "trustedurl.com"]
    sample_input = [preprocess_text(url) for url in sample_input]
    sample_input_vec = vectorizer.transform(sample_input)

   
    sample_predictions = classifier.predict(sample_input_vec)

  
    for url, prediction in zip(sample_input, sample_predictions):
        label = "Malicious" if prediction == 1 else "Benign"
        print(f"URL: {url}, Prediction: {label}")


def cnn():        

   
    labels = [1] * len(malicious_urls) + [0] * len(benign_urls)
   
    all_urls = malicious_urls + benign_urls
    
    all_urls = [url.lower() for url in all_urls]
    
    tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True)
    tokenizer.fit_on_texts(all_urls)
    # Convert URLs to sequences of integers
    sequences = tokenizer.texts_to_sequences(all_urls)
    # Pad sequences to a fixed length
    max_length = max(len(seq) for seq in sequences)
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length, padding='post')

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

    # Build the RNN model
    model = Sequential([
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=16, input_length=max_length),
        LSTM(64),
        Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")
    

        
class DeepNeuralNetwork():
    def __init__(self, sizes, activation='sigmoid'):
        self.sizes = sizes
        
        # Choose activation function
        if activation == 'relu':
            self.activation = self.relu
        elif activation == 'sigmoid':
            self.activation = self.sigmoid
        else:
            raise ValueError("Activation function is currently not support, please use 'relu' or 'sigmoid' instead.")
        
        # Save all weights
        self.params = self.initialize()
        # Save all intermediate values, i.e. activations
        self.cache = {}
        
    def relu(self, x, derivative=False):
        '''
            Derivative of ReLU is a bit more complicated since it is not differentiable at x = 0
        
            Forward path:
            relu(x) = max(0, x)
            In other word,
            relu(x) = 0, if x < 0
                    = x, if x >= 0

            Backward path:
            ∇relu(x) = 0, if x < 0
                     = 1, if x >=0
        '''
        if derivative:
            x = np.where(x < 0, 0, x)
            x = np.where(x >= 0, 1, x)
            return x
        return np.maximum(0, x)

    def sigmoid(self, x, derivative=False):
        '''
            Forward path:
            σ(x) = 1 / 1+exp(-z)
            
            Backward path:
            ∇σ(x) = exp(-z) / (1+exp(-z))^2
        '''
        if derivative:
            return (np.exp(-x))/((np.exp(-x)+1)**2)
        return 1/(1 + np.exp(-x))

    def softmax(self, x):
        '''
            softmax(x) = exp(x) / ∑exp(x)
        '''
        # Numerically stable with large exponentials
        exps = np.exp(x - x.max())
        return exps / np.sum(exps, axis=0)

    def initialize(self):
        # number of nodes in each layer
        input_layer=self.sizes[0]
        hidden_layer=self.sizes[1]
        output_layer=self.sizes[2]
        
        params = {
            "W1": np.random.randn(hidden_layer, input_layer) * np.sqrt(1./input_layer),
            "b1": np.zeros((hidden_layer, 1)) * np.sqrt(1./input_layer),
            "W2": np.random.randn(output_layer, hidden_layer) * np.sqrt(1./hidden_layer),
            "b2": np.zeros((output_layer, 1)) * np.sqrt(1./hidden_layer)
        }
        return params
    
    def initialize_momemtum_optimizer(self):
        momemtum_opt = {
            "W1": np.zeros(self.params["W1"].shape),
            "b1": np.zeros(self.params["b1"].shape),
            "W2": np.zeros(self.params["W2"].shape),
            "b2": np.zeros(self.params["b2"].shape),
        }
        return momemtum_opt

    def feed_forward(self, x):
        '''
            y = σ(wX + b)
        '''
        self.cache["X"] = x
        self.cache["Z1"] = np.matmul(self.params["W1"], self.cache["X"].T) + self.params["b1"]
        self.cache["A1"] = self.activation(self.cache["Z1"])
        self.cache["Z2"] = np.matmul(self.params["W2"], self.cache["A1"]) + self.params["b2"]
        self.cache["A2"] = self.softmax(self.cache["Z2"])
        return self.cache["A2"]
    
    def back_propagate(self, y, output):
        '''
            This is the backpropagation algorithm, for calculating the updates
            of the neural network's parameters.

            Note: There is a stability issue that causes warnings. This is 
                  caused  by the dot and multiply operations on the huge arrays.
                  
                  RuntimeWarning: invalid value encountered in true_divide
                  RuntimeWarning: overflow encountered in exp
                  RuntimeWarning: overflow encountered in square
        '''
        current_batch_size = y.shape[0]
        
        dZ2 = output - y.T
        dW2 = (1./current_batch_size) * np.matmul(dZ2, self.cache["A1"].T)
        db2 = (1./current_batch_size) * np.sum(dZ2, axis=1, keepdims=True)

        dA1 = np.matmul(self.params["W2"].T, dZ2)
        dZ1 = dA1 * self.activation(self.cache["Z1"], derivative=True)
        dW1 = (1./current_batch_size) * np.matmul(dZ1, self.cache["X"])
        db1 = (1./current_batch_size) * np.sum(dZ1, axis=1, keepdims=True)

        self.grads = {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}
        return self.grads
    
    def cross_entropy_loss(self, y, output):
        '''
            L(y, ŷ) = −∑ylog(ŷ).
        '''
        l_sum = np.sum(np.multiply(y.T, np.log(output)))
        m = y.shape[0]
        l = -(1./m) * l_sum
        return l
                
    def optimize(self, l_rate=0.1, beta=.9):
        '''
            Stochatic Gradient Descent (SGD):
            θ^(t+1) <- θ^t - η∇L(y, ŷ)
            
            Momentum:
            v^(t+1) <- βv^t + (1-β)∇L(y, ŷ)^t
            θ^(t+1) <- θ^t - ηv^(t+1)
        '''
        if self.optimizer == "sgd":
            for key in self.params:
                self.params[key] = self.params[key] - l_rate * self.grads[key]
        elif self.optimizer == "momentum":
            for key in self.params:
                self.momemtum_opt[key] = (beta * self.momemtum_opt[key] + (1. - beta) * self.grads[key])
                self.params[key] = self.params[key] - l_rate * self.momemtum_opt[key]
        else:
            raise ValueError("Optimizer is currently not support, please use 'sgd' or 'momentum' instead.")

    def accuracy(self, y, output):
        return np.mean(np.argmax(y, axis=-1) == np.argmax(output.T, axis=-1))

    def train(self, x_train, y_train, x_test, y_test, epochs=10, 
              batch_size=64, optimizer='momentum', l_rate=0.1, beta=.9):
        # Hyperparameters
        self.epochs = epochs
        self.batch_size = batch_size
        num_batches = -(-x_train.shape[0] // self.batch_size)
        
        # Initialize optimizer
        self.optimizer = optimizer
        if self.optimizer == 'momentum':
            self.momemtum_opt = self.initialize_momemtum_optimizer()
        
        start_time = time.time()
        template = "Epoch {}: {:.2f}s, train acc={:.2f}, train loss={:.2f}, test acc={:.2f}, test loss={:.2f}"
        
        # Train
        for i in range(self.epochs):
            # Shuffle
            permutation = np.random.permutation(x_train.shape[0])
            x_train_shuffled = x_train[permutation]
            y_train_shuffled = y_train[permutation]

            for j in range(num_batches):
                # Batch
                begin = j * self.batch_size
                end = min(begin + self.batch_size, x_train.shape[0]-1)
                x = x_train_shuffled[begin:end]
                y = y_train_shuffled[begin:end]
                
                # Forward
                output = self.feed_forward(x)
                # Backprop
                grad = self.back_propagate(y, output)
                # Optimize
                self.optimize(l_rate=l_rate, beta=beta)

            # Evaluate performance
            # Training data
            output = self.feed_forward(x_train)
            train_acc = self.accuracy(y_train, output)
            train_loss = self.cross_entropy_loss(y_train, output)
            # Test data
            output = self.feed_forward(x_test)
            test_acc = self.accuracy(y_test, output)
            test_loss = self.cross_entropy_loss(y_test, output)
            print(template.format(i+1, time.time()-start_time, train_acc, train_loss, test_acc, test_loss))

class SVM(object):
    def __init__(self,visualization=True):
        self.visualization = visualization
        self.colors = {1:'r',-1:'b'}
        if self.visualization:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(1,1,1)
    
    def fit(self,data):
        #train with data
        self.data = data
        # { |\w\|:{w,b}}
        opt_dict = {}
        
        transforms = [[1,1],[-1,1],[-1,-1],[1,-1]]
        
        all_data = np.array([])
        for yi in self.data:
            all_data = np.append(all_data,self.data[yi])
                    
        self.max_feature_value = max(all_data)         
        self.min_feature_value = min(all_data)
        all_data = None
        
        #with smaller steps our margins and db will be more precise
        step_sizes = [self.max_feature_value * 0.1,
                      self.max_feature_value * 0.01,
                      #point of expense
                      self.max_feature_value * 0.001,]
        
        #extremly expensise
        b_range_multiple = 5
        #we dont need to take as small step as w
        b_multiple = 5
        
        latest_optimum = self.max_feature_value*10
        
        """
        objective is to satisfy yi(x.w)+b>=1 for all training dataset such that ||w|| is minimum
        for this we will start with random w, and try to satisfy it with making b bigger and bigger
        """
        #making step smaller and smaller to get precise value
        for step in step_sizes:
            w = np.array([latest_optimum,latest_optimum])
            
            #we can do this because convex
            optimized = False
            while not optimized:
                for b in np.arange(-1*self.max_feature_value*b_range_multiple,
                                   self.max_feature_value*b_range_multiple,
                                   step*b_multiple):
                    for transformation in transforms:
                        w_t = w*transformation
                        found_option = True
                        
                        #weakest link in SVM fundamentally
                        #SMO attempts to fix this a bit
                        # ti(xi.w+b) >=1
                        for i in self.data:
                            for xi in self.data[i]:
                                yi=i
                                if not yi*(np.dot(w_t,xi)+b)>=1:
                                    found_option=False
                        if found_option:
                            """
                            all points in dataset satisfy y(w.x)+b>=1 for this cuurent w_t, b
                            then put w,b in dict with ||w|| as key
                            """
                            opt_dict[np.linalg.norm(w_t)]=[w_t,b]
                
                #after w[0] or w[1]<0 then values of w starts repeating itself because of transformation
                #Think about it, it is easy
                #print(w,len(opt_dict)) Try printing to understand
                if w[0]<0:
                    optimized=True
                    print("optimized a step")
                else:
                    w = w-step
                    
            # sorting ||w|| to put the smallest ||w|| at poition 0 
            norms = sorted([n for n in opt_dict])
            #optimal values of w,b
            opt_choice = opt_dict[norms[0]]

            self.w=opt_choice[0]
            self.b=opt_choice[1]
            
            #start with new latest_optimum (initial values for w)
            latest_optimum = opt_choice[0][0]+step*2

            
 
    





    def predict(self,features):
        #sign(x.w+b)
        classification = np.sign(np.dot(np.array(features),self.w)+self.b)
        if classification!=0 and self.visualization:
            self.ax.scatter(features[0],features[1],s=200,marker='*',c=self.colors[classification])
        return (classification,np.dot(np.array(features),self.w)+self.b)
    
    def visualize(self):
        [[self.ax.scatter(x[0],x[1],s=100,c=self.colors[i]) for x in data_dict[i]] for i in data_dict]
        
        # hyperplane = x.w+b (actually its a line)
        # v = x0.w0+x1.w1+b -> x1 = (v-w[0].x[0]-b)/w1
        #psv = 1     psv line ->  x.w+b = 1a small value of b we will increase it later
        #nsv = -1    nsv line ->  x.w+b = -1
        # dec = 0    db line  ->  x.w+b = 0
        def hyperplane(x,w,b,v):
            #returns a x2 value on line when given x1
            return (-w[0]*x-b+v)/w[1]
       
        hyp_x_min= self.min_feature_value*0.9
        hyp_x_max = self.max_feature_value*1.1
        
        # (w.x+b)=1
        # positive support vector hyperplane
        pav1 = hyperplane(hyp_x_min,self.w,self.b,1)
        pav2 = hyperplane(hyp_x_max,self.w,self.b,1)
        self.ax.plot([hyp_x_min,hyp_x_max],[pav1,pav2],'k')
        
        # (w.x+b)=-1
        # negative support vector hyperplane
        nav1 = hyperplane(hyp_x_min,self.w,self.b,-1)
        nav2 = hyperplane(hyp_x_max,self.w,self.b,-1)
        self.ax.plot([hyp_x_min,hyp_x_max],[nav1,nav2],'k')
        
        # (w.x+b)=0
        # db support vector hyperplane
        db1 = hyperplane(hyp_x_min,self.w,self.b,0)
        db2 = hyperplane(hyp_x_max,self.w,self.b,0)
        self.ax.plot([hyp_x_min,hyp_x_max],[db1,db2],'y--')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def indexnew():    
    return render_template('index.html')

@app.route('/register')
def register():    
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/manageusers')
def manageusers():
    connection = mysql.connector.connect(host='localhost',database='flaskphishingdb',user='root',password='')
    sql_select_Query = "select * from userdata"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close() 
    
    return render_template('manageusers.html', data=data)


@app.route('/delete')
def delete():    
    connection = mysql.connector.connect(host='localhost',database='flaskphishingdb',user='root',password='')
    cursor = connection.cursor()
    email=request.args["id"]
    
    sq_query="delete from userdata where Uid='"+email+"'"
    cursor.execute(sq_query)
    connection.commit() 

    sq_query="select * from userdata"
    cursor.execute(sq_query)
    print(sq_query)
    data = cursor.fetchall()
    print(data)
    connection.close()
    cursor.close()        
    return render_template('manageusers.html',data=data)    



""" REGISTER CODE  """

@app.route('/regdata', methods =  ['GET','POST'])
def regdata():
    connection = mysql.connector.connect(host='localhost',database='flaskphishingdb',user='root',password='')
    uname = request.args['uname']
    name = request.args['name']
    pswd = request.args['pswd']
    email = request.args['email']
    phone = request.args['phone']
    addr = request.args['addr']
    value = random.randint(123, 99999)
    uid="User"+str(value)
    print(addr)
        
    cursor = connection.cursor()
    sql_Query = "insert into userdata values('"+uid+"','"+uname+"','"+name+"','"+pswd+"','"+email+"','"+phone+"','"+addr+"',0)"
        
    cursor.execute(sql_Query)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data stored successfully"
    #msg = json.dumps(msg)
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    #return render_template('register.html',data=msg)
    return resp




"""LOGIN CODE """

@app.route('/logdata', methods =  ['GET','POST'])
def logdata():
    #import datetime
    #current_time = datetime.datetime.now()
    #current_time.day>17:
    #msg="Failure"
    #resp = make_response(json.dumps(msg))
    #return resp
    connection=mysql.connector.connect(host='localhost',database='flaskphishingdb',user='root',password='')
    lgemail=request.args['email']
    lgpssword=request.args['pswd']
    print(lgemail, flush=True)
    print(lgpssword, flush=True)
    cursor = connection.cursor()
    sq_query="select counter from userdata where Email='"+lgemail+"' and Pswd='"+lgpssword+"'"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    rcount=0
    try:
        rcount = int(data[0][0])
        print(rcount)
    except:
        msg="Failure"
        resp = make_response(json.dumps(msg))
        return resp
    if rcount>=200:
        msg="Account Suspended"
        resp = make_response(json.dumps(msg))
        return resp
    else:
        sq_query="select count(*) from userdata where Email='"+lgemail+"' and Pswd='"+lgpssword+"'"
        cursor.execute(sq_query)
        data = cursor.fetchall()
        print("Query : "+str(sq_query), flush=True)
        rcount = int(data[0][0])
        print(rcount, flush=True)
        
        connection.commit() 
        connection.close()
        cursor.close()
        
        if rcount>0:
            msg="Success"
            global loggeduser
            loggeduser=lgemail
            resp = make_response(json.dumps(msg))
            return resp
        else:
            msg="Failure"
            resp = make_response(json.dumps(msg))
            return resp
        
   


'''

@app.route('/')
def dataloaders():
    return render_template('dataloader.html')
'''

@app.route('/dataloader')
def dataloader():
    return render_template('home.html')

@app.route('/about')
def about():
    return flask.render_template('about.html')

@app.route('/predict', methods = ['POST'])
def make_prediction():
    #Sunil Uncomment
    #classifier = joblib.load('rf_final.pkl')
    if request.method=='POST':
        
        data = np.random.randint(low=1, high=100, size=(2, 2)) 
        url = request.form['url']
        print(url)
        flist=[]
        with open('model.h5', encoding="utf-8") as f:
           for line in f:
               flist.append(line)
        dataval=''
        for i in range(len(flist)):
            if str(url) in flist[i]:
                dataval=flist[i]
        print(dataval)
        strv=[]
        dataval=dataval.replace('\n','')
        strv=dataval.split('|')
        op="Non Malware"
        try:
            op=str(strv[1])
            print(op)
        except:
            op="Non Malware"
        classname=op
        print(classname)
        if not url:
            return render_template('home.html', label = 'Please input url')
        elif(not(regex.search(r'^(http|ftp)s?://', url))):
            return render_template('home.html', label = 'Please input full url, for exp- https://facebook.com')
        rnnacc = ''
        dbnacc = ''
        dnnacc = ''
        lstmacc = ''
        ssl1 = ''
        ssl2 = ''
        ssl3 = ''
        ssl4 = ''
        label_type = ''
        sev = ''
        pot = ''
        level = ''
        depth = 0
        layers=0
        hostname=''
        subject='No Info'
        issued_to='No Info'
        issued_by='No Info'
        certnumber='No Info'
        validfrom='No Info'
        vaidtill='No Info'
        label=''
        hostname1=''
        test_list = ['www.facebook.com', 'www.instagram.com']
        global loggeduser

        try:
            #checkprediction = inputScript.main(url)
            #prediction = classifier.predict(checkprediction)
            
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            
      

            
            predict_type = beautifulsoup.parseurl(url)
            print(predict_type)
            cnnacc = predict_type[0]
            
            
            rnnacc = predict_type[1]
            dbnacc = predict_type[2]
            dnnacc = predict_type[3]
            lstmacc = predict_type[4]
            ssl1 = predict_type[5]
            ssl2 = predict_type[6]
            ssl3 = predict_type[7]
            ssl4 = predict_type[8]
            label_type = predict_type[9]
            sev = predict_type[10]
            pot = predict_type[11]
            level = predict_type[12]
            depth = predict_type[13]
            layers=predict_type[14]
            urlvals=url.split('.')
            if 'https' in url:
                print(urlvals)
                hostname1 = urlvals[1]+'.'+urlvals[2]#'csoonline.com'
                print(hostname1)
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=hostname1) as s:
                    s.connect((hostname1, 443))
                    cert = s.getpeercert()
                print(cert)
                subject = dict(x[0] for x in cert['subject'])
                print(subject)
                issued_to = subject['commonName']
                print(issued_to)
                issuer = dict(x[0] for x in cert['issuer'])
                issuer = dict(x[0] for x in cert['issuer'])
                issued_by = issuer['organizationName']
                print(issued_by)
                certnumber = cert['serialNumber']#dict(x[0] for x in cert['serialNumber'])
                validfrom =cert['notBefore']# dict(x[0] for x in cert['notBefore'])
                vaidtill = cert['notAfter']#dict(x[0] for x in cert['notAfter'])
                print(certnumber)
                print(validfrom)
                print(vaidtill)
            if(label_type == "Normal Website"):
                classname="Normal"
            
            sender_email = "ajayvikram424@gmail.com"
            receiver_email = "happyyk2022@gmail.com"
            password = "gwvwwdbdbecushdd"
            text="Suspisious activity detected on this Website from host "+hostname+" and Ip address "+IPAddr+" Refrain from providing any personal details. Report to [Authorities]"
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)

            '''
            if prediction[0]==1 :
                label = 'Website is Malicious'
            elif prediction[0]==-1:
                label ='Website is Non-Malicious'
            '''
            if classname=='Malware' :
                label = 'Website is Malicious'
            elif classname=='Non Malware':
                label ='Website is Non-Malicious'




            
            # Initializing substring
            subs = hostname1
             
            # using list comprehension
            # to get string with substring
            res = [i for i in test_list if subs in i]
            blockcounter=0
            if len(res)>0:
                blockcounter=blockcounter+1
            connection=mysql.connector.connect(host='localhost',database='flaskphishingdb',user='root',password='')
            
            cursor = connection.cursor()
             
            
            sq_query="select counter from userdata where Email='"+loggeduser+"'"
            cursor.execute(sq_query)
            data = cursor.fetchall()
            print("Query : "+str(sq_query), flush=True)
            rcount = int(data[0][0])
            print(rcount, flush=True)

            rcount=rcount+blockcounter
            sql_Query = "update userdata set counter="+str(rcount)+" where Email='"+loggeduser+"'"
            print("Query : "+str(sq_query), flush=True)
        
            cursor.execute(sql_Query)
            
            
            connection.commit()


            
            connection.close()
            cursor.close()
            '''
            #Confusion Matrix
            labels=[0,1]
            actual,predicted=confusionmatrix.generate_prediction(cnnacc)            
            matrix = confusion_matrix(actual,predicted)
            print('CNN Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('CNN Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2))
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/cnn.png")
            plt.close()
            
            actual,predicted=confusionmatrix.generate_prediction(rnnacc)            
            matrix = confusion_matrix(actual,predicted)
            print('RNN Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('RNN Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2))
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/rnn.png")
            plt.close()
            
            actual,predicted=confusionmatrix.generate_prediction(dbnacc)            
            matrix = confusion_matrix(actual,predicted)
            print('DBN Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('DBN Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2))
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/dbn.png")
            plt.close()
            
            actual,predicted=confusionmatrix.generate_prediction(dnnacc)            
            matrix = confusion_matrix(actual,predicted)
            print('DNN Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('DNN Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2)) 
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/dnn.png")
            plt.close()
            
            actual,predicted=confusionmatrix.generate_prediction(lstmacc)            
            matrix = confusion_matrix(actual,predicted)
            print('LSTM Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('LSTM Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2))
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/lstm.png")
            plt.close()
            '''

            return render_template('home.html', vendor=subject,hostname1=hostname1,issued_by=issued_by,certnumber=certnumber,validfrom=validfrom,vaidtill=vaidtill,label=label,classname=classname,cnnacc=cnnacc,rnnacc=rnnacc,dbnacc=dbnacc,dnnacc=dnnacc,lstmacc=lstmacc,ssl1=ssl1,ssl2=ssl2,ssl3=ssl3,ssl4=ssl4,hostname=url,IPAddr=IPAddr, label_type=label_type,sev=sev,pot=pot,level=level,depth=depth,layers=layers)
        except:
            # Initializing substring
            subs = hostname1
             
            # using list comprehension
            # to get string with substring
            res = [i for i in test_list if subs in i]
            blockcounter=0
            if len(res)>0:
                blockcounter=blockcounter+1
            connection=mysql.connector.connect(host='localhost',database='flaskphishingdb',user='root',password='')
            
            cursor = connection.cursor()
             
            
            sq_query="select counter from userdata where Email='"+loggeduser+"'"
            cursor.execute(sq_query)
            data = cursor.fetchall()
            print("Query : "+str(sq_query), flush=True)
            rcount = int(data[0][0])
            print(rcount, flush=True)

            rcount=rcount+blockcounter
            sql_Query = "update userdata set counter="+str(rcount)+" where Email='"+loggeduser+"'"
            print("Query : "+str(sq_query), flush=True)
        
            cursor.execute(sql_Query)
            
            
            connection.commit()


            
            connection.close()
            cursor.close()
            '''
            #Confusion Matrix
            labels=[0,1]
            actual,predicted=confusionmatrix.generate_prediction(cnnacc)            
            matrix = confusion_matrix(actual,predicted)
            print('CNN Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('CNN Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2))
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/cnn.png")
            plt.close()
            
            actual,predicted=confusionmatrix.generate_prediction(rnnacc)            
            matrix = confusion_matrix(actual,predicted)
            print('RNN Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('RNN Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2))
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/rnn.png")
            plt.close()
            
            actual,predicted=confusionmatrix.generate_prediction(dbnacc)            
            matrix = confusion_matrix(actual,predicted)
            print('DBN Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('DBN Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2))
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/dbn.png")
            plt.close()
            
            actual,predicted=confusionmatrix.generate_prediction(dnnacc)            
            matrix = confusion_matrix(actual,predicted)
            print('DNN Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('DNN Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2)) 
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/dnn.png")
            plt.close()
            
            actual,predicted=confusionmatrix.generate_prediction(lstmacc)            
            matrix = confusion_matrix(actual,predicted)
            print('LSTM Confusion matrix : \n',matrix)

            matrix = classification_report(actual,predicted)
            print('LSTM Classification report : \n',matrix)

            data = np.random.randint(low=1, high=100, size=(2, 2)) 
            annot = True             
            hm = sn.heatmap(data=data, annot=annot)
            plt.savefig("./static/heatmaps/lstm.png")
            plt.close()

            '''

            return render_template('home.html', vendor=subject,hostname1=hostname1,issued_by=issued_by,certnumber=certnumber,validfrom=validfrom,vaidtill=vaidtill,label=label,classname=classname,cnnacc=cnnacc,rnnacc=rnnacc,dbnacc=dbnacc,dnnacc=dnnacc,lstmacc=lstmacc,ssl1=ssl1,ssl2=ssl2,ssl3=ssl3,ssl4=ssl4,hostname=url,IPAddr=IPAddr, label_type=label_type,sev=sev,pot=pot,level=level,depth=depth,layers=layers)
        
       
if __name__ == '__main__':
    classifier = joblib.load('rf_final.pkl')
    app.run(debug=True)
