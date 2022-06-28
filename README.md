![](banner.png)

# Workshop repository
This is the repository for the workshop "AI-assisted Newsletter Dashboard" that was held during the datalift summit. It is self-containing, such that you can reproduce all steps from the workshop :)

To do so, please also look into the file `slides.pdf`. If you have any further questions, please don't hesitate to contact:
- moritz.feuerpfeil@kern.ai, main contributor to this workshop
- johannes.hoetter@kern.ai, co-founder of Kern AI

## Repository Structure
In this repository you will find all the necessary files to follow along. This repo is organzied as the following:
- The folder structure represents our workshop outline, starting with 01_MailExport
- The directories where we code are organized in three sub-categories
  - **scratch**: necessary files but only filled with comments if you want to code along the whole journey
  - **guided**: necessary files with some code filled in for a more relaxed follow along
  - **finished**: the solution we provide for the next step
- We provide all the necessary data for the following steps in the **finished** sub-directories

## Installation
### Repository and Environment
1. clone this repository or download it as a zip
2. (if you don't have anaconda installed) [install anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
3. (recommended) create a new conda environment
    ```
    $ conda create --name datalift python=3.8
    $ conda activate datalift
    ```
4. install the requirements
    ```
    $ pip install -r requirements.txt
    ```

### IDE
We strongly recommend using [VSCode](https://code.visualstudio.com/download) as your IDE. 

**Necessary** Extensions:
- Jupyter
- Python

*Suggested* Extensions:
- Rainbow CSV
- Material Icon Theme

## Running this Repo
To run the fastAPI backend and streamlit frontend, please follow these two steps:
1. go into 06_FastAPI/finished and type
    ```
    $ uvicorn main:app --reload
    ```
    or (if the previous does not work)
    ```
    $ python -m uvicorn main:app --reload
    ```
2. go into 05_Streamlit/finished and type
    ```
    $ streamlit run app.py
    ```
   
You're now up and running! Make sure to use streamlit in "wide mode", which you can change in the settings that you can access on the top right of your UI.

## Exemplary potential improvements
The app developed in the 3 hours workshop is not perfect yet. Take the following list as an example for things on how you can improve the app further on your own:

![](https://user-images.githubusercontent.com/57487741/175494769-e4f3a6c0-9d03-41e0-a990-8d70edcb8943.png)

## Timetable of the workshop
| Topic                                                           | Time   |
| --------------------------------------------------------------- | ------ |
| 📧 collecting data with oauth2 in GMail                          | 15 min |
| 🔧 processing data (e.g. HTML and text parsing)                  | 30 min |
| 🔖 building training data for topic modelling                    | 15 min |
| 🧠 applying transfer learning with transformers and recommenders | 30 min |
| ☕ **break** ☕                                                   | 10 min |
| 👑 building a streamlit UI                                       | 40 min |
| 👾 building a minimal backend via FastAPI                        | 40 min |
