## Inspiration
This project was inspired by a desire to impact healthcare, particularly given that over 1 in 6 people in Ontario lack access to a primary care physician, with average specialist wait times of 11 weeks. The rise of telemedicine highlighted the potential of virtual solutions, leading us to create a digital tool that requires no human intervention. We focused on acne due to its prevalence, especially among youth, and its effect on self-esteem. Our goal is to improve lives while easing the workload for physicians.

## What it does
spotSpot works by simply taking an image of your face. Users can choose to take a Live Photo, or upload an existing one. spotSpot then analyzes the image, and informs the user of their specific acne type, as well as next-steps in terms of improving their condition. Our recommendations and advice are limited to specific chemicals or treatments, as opposed to brands. Additionally, we only recommend treatments that can be obtained Over-the-Counter (OTC), without a prescription.

## How we built it
We built this classifier in Python using PyTorch's ShuffleNet Conventional Neural Network as it was the most effective and efficient for our training data, especially since our dataset was small. By taking the labelled images as a training set for our classification, we were able to augment each training picture with our model and improve accuracy when we ran full face scans. We fine-tuned our training model to improve accuracy while mitigating overfitting by implementing weights to all of the different acne classes depending on the number of training images as well as finding the optimal training-reruns using trial and error.

Devpost Link: https://devpost.com/software/spotspot-gdfxez?ref_content=my-projects-tab&ref_feature=my_projects

## Setup
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