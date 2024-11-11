Inspiration
This project was born through a desire to impact the field of healthcare. As of July 2024, over 1 in 6 people in Ontario do not have access to a primary care physician. On top of that, specialist wait times are long, with patients waiting an average of 11 weeks after a GP referral to see a specialist. Even in "urgent" cases, patients still wait an average of 7 weeks to get the help they need. After seeing the rise of telemedicine in recent years, as well as its convenience in being able to help patients virtually, we were inspired to create our own digital solution. The key difference is, our creation doesn't require a doctor, or any other human intervention, even. We chose to target acne as a condition specifically, due to its prevalence (especially among youth) and its impact on self-esteem and confidence, which affects overall quality of life. This project was our attempt at creating a real impact on people's lives, while simultaneously alleviating some stress/workload for physicians.

What it does
spotSpot works by simply taking an image of your face. Users can choose to take a Live Photo, or upload an existing one. spotSpot then analyzes the image, and informs the user of their specific acne type, as well as next-steps in terms of improving their condition. Our recommendations and advice are limited to specific chemicals or treatments, as opposed to brands. Additionally, we only recommend treatments that can be obtained Over-the-Counter (OTC), without a prescription.

How we built it
We built this classifier in Python using PyTorch's ShuffleNet Conventional Neural Network as it was the most effective and efficient for our training data, especially since our dataset was small. By taking the labelled images as a training set for our classification, we were able to augment each training picture with our model and improve accuracy when we ran full face scans. We fine-tuned our training model to improve accuracy while mitigating overfitting by implementing weights to all of the different acne classes depending on the number of training images as well as finding the optimal training-reruns using trial and error.

Devpost Link: https://devpost.com/software/spotspot-gdfxez?ref_content=my-projects-tab&ref_feature=my_projects

Setup
1. Git Clone
Clone the repository in your local machine using the following command:

```git clone https://github.com/tonizeng/spotSpot.git```

2. Change the directory to spotSpot by:

```cd spotSpot```

3. Install requirements
Install the requirements using the following command:

```pip install -r requirements.txt```

3. To run the app, use the following command:

```streamlit run main.py```

or

```python -m streamlit run main.py```