
from flask import Flask, render_template, request
import re
import os
import openai

app = Flask(__name__)

openai.api_key = "YOUR_API_KEY"
model="gpt-3.5-turbo-16k"


def product_manager(project_name, project_description, technologies):
    project_folder = os.path.join("projects", project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    product_details_file = os.path.join(project_folder, "product_details.txt")   
    if not os.path.exists(product_details_file):

        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[


                {"role": "system", "content": """Forget everything that was said to you before. Now we will play a game with you.
                        You are ProductGPT, a product developer Artificial Intelligence model. 
                        Your most important and only task; ProjectGPT, the project manager of a software house, supported the application, 
                        which was briefly explained to you in the first message by the user and wanted to be developed, with the information in hand 
                        and the features of similar applications you know, and even answering the question what features would you like to have in such an application 
                        if you were a user. don't tell. Here's the thing you need to pay attention to: You should describe this project in as much detail as possible, 
                        and be very clear about the features you want and don't want. You should not forget that; This information received from you will start 
                        an artificial intelligence project called ProjectGPT. That's why you should be clear and complete in your definition."""},
                {"role": "user", "content": project_description},
                {"role": "user", "content": technologies}
            ],
            temperature=1.5,
            
        )
        product_details = response.choices[0].message['content'].strip()
        with open(product_details_file, "w", encoding="utf-8") as f:
            f.write(product_details)
    else:
        with open(product_details_file, "r", encoding="utf-8") as f:
            product_details = f.read().strip()
    
    return product_details


   

def project_manager(project_name):
    project_folder = os.path.join("projects", project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    product_details_file = os.path.join(project_folder, "product_details.txt") 
    with open(product_details_file, "r", encoding="utf-8") as f:
        product_details = f.read().strip()

    project_details_file = os.path.join(project_folder, "project_details.txt")   
    if not os.path.exists(project_details_file):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
    messages=[


                {"role": "system", "content": """You are the best project manager ever. You should consider all the possibilities for the development of a flask-based python application, and accordingly, 
                you should delegate the necessary tasks to the following departments in as much detail as possible, in order to best develop the application that you are given details and wants to be developed. 
                Your answer should be in a list. The Application Tree should be at the top of this list. This tree should contain the application directory, a detailed version of the folders and files that should be in this directory.
                This will be the skeleton of the application to be developed and all other departments will create and save the necessary files according to this template.
                The tasks that these departments should do and the details of each task should be included in this list. The information you provide must be complete. This information received from you will start a whole project. 
                That's why I want you to explain all the steps in the most detailed way possible. 
                You are the head of this project and you have only one right to communicate with the staff of this project. So answer with as much detail as you can. Push your limits. 
                The task lists of each department should be XXXXX before they start, 
                and then the department name and START should be written and again XXXXX. should be followed by the department name and END, and it should be XXXXX. 
                Example Message Format:
                  XXXXX Application Tree START XXXXX
                   Application Tree: 
                    .
                    .
                    .
                  XXXXX Application Tree END XXXXX
                  XXXXX UI/UX DESIGN START XXXXX
                  ...
                  XXXXX UI/UX DESIGN END XXXXX
                  .
                  .
                  .
                  XXXXX FRONTEND START XXXXX
                  ...
                  XXXXX FRONTEND END XXXXX

                Departments:
                UI/UX DESIGN
                DATABASE
                BACKEND
                FRONTEND"""},
                {"role": "user", "content": product_details}
            ],
            temperature=1.4,
            
        )
        project_details = response.choices[0].message['content'].strip()
        with open(project_details_file, "w", encoding="utf-8") as f:
            f.write(project_details)
    else:
        with open(project_details_file, "r", encoding="utf-8") as f:
            project_details = f.read().strip()
    
    return project_details
import os




def pmformater(project_name):
    # Düzenli ifade ile etiketleri tespit etme
    project_folder = os.path.join("projects", project_name)
    project_details_file = os.path.join(project_folder, "project_details.txt") 
    with open(project_details_file, "r", encoding="utf-8") as f:
            project_details = f.read().strip()


    labels = re.findall(r'X{3,}.*?X{3,}', project_details)
    
    # "START" ve "END" etiketleri arasında kalan içeriği saklayalım
    sections_to_keep = []
    for i in range(0, len(labels) - 1, 2):
        start_label = labels[i]
        if i + 1 < len(labels):
            end_label = labels[i + 1]
            section_content = re.search(re.escape(start_label) + r'(.*?)' + re.escape(end_label), project_details, re.DOTALL)
            if section_content:
                sections_to_keep.append(section_content.group(0))
    
    refined_response = "\n".join(sections_to_keep)
    
    for label in labels:
        # Eğer label "START" veya "END" içermiyorsa bu label'ı atlayalım
        if "START" not in label and "END" not in label:
            continue
        
        start_x_count = len(re.findall(r'^X+', label)[0])
        end_x_count = len(re.findall(r'X+$', label)[0])
        
        # Eğer etiket başında veya sonunda 5'ten az "X" karakteri varsa, eksik olanları ekleyelim
        if start_x_count < 5 or end_x_count < 5:
            corrected_label = "X" * (5 - start_x_count) + label + "X" * (5 - end_x_count)
            refined_response = refined_response.replace(label, corrected_label)
    
    # "START" ve "END" arasında bir boşluk ekleyelim
    project_folder = os.path.join("projects", project_name)
    formated_project_details = refined_response.replace("STARTXXXXX", "START XXXXX").replace("ENDXXXXX", "END XXXXX")
    formated_project_details_file = os.path.join(project_folder, "formated_project_details.txt")   
    if not os.path.exists(formated_project_details_file):
        with open(formated_project_details_file, "w", encoding="utf-8") as f:
            f.write(formated_project_details)    
    return formated_project_details



  
def pm_split_and_save(project_name):
    # Bölüm başlangıç ve bitiş tanımlamaları
    sections = {
        'XXXXX Application Tree START XXXXX': 'tree.txt',
        'XXXXX UI/UX DESIGN START XXXXX': 'ui.txt',
        'XXXXX DATABASE START XXXXX': 'database.txt',
        'XXXXX BACKEND START XXXXX': 'backend.txt',
        'XXXXX FRONTEND START XXXXX': 'frontend.txt'
    }
    end_sections = set([key.replace('START', 'END') for key in sections.keys()])

    # Oluşturulan dosyaların yollarını saklamak için bir liste tanımlayalım
    created_files_pm = []

    # Dosyayı okuma
    project_folder = os.path.join("projects", project_name)
    formated_project_details_file = os.path.join(project_folder, "formated_project_details.txt") 
    with open(formated_project_details_file, 'r') as file:
        lines = file.readlines()

    current_file_name = None
    for line in lines:
        stripped_line = line.strip()
        if stripped_line in sections:
            if current_file_name:
                current_file.close()
            # Dosyaları formated_project_details_file değişkeninin bulunduğu klasörde oluşturalım
            current_file_name = os.path.join(os.path.dirname(formated_project_details_file), sections[stripped_line])
            created_files_pm.append(current_file_name)
            current_file = open(current_file_name, 'w')
        elif stripped_line in end_sections:
            if current_file_name:
                current_file.close()
                current_file_name = None
        elif current_file_name:
            current_file.write(line)

    if current_file_name:
        current_file.close()

    # Oluşturduğumuz dosyaların yollarını döndürelim
    return created_files_pm


def junior1_ui_designer(project_name):
    # Bu fonksiyon, UI/UX tasarımı ile ilgili temel adımları belirtir.
    project_folder = os.path.join("projects", project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    junior1_ui_designer_file = os.path.join(project_folder, "junior1_ui_design.txt")  

    project_file_ui = os.path.join(project_folder, "ui.txt") 
    with open(project_file_ui, 'r') as f:   
        project_file_ui=f.read().strip()

    Application_tree = os.path.join(project_folder, "tree.txt") 
    with open(Application_tree, 'r') as f:   
        Application_tree=f.read().strip()

    if not os.path.exists(junior1_ui_designer_file):
        # OpenAI API'si için detaylı sistem promptu

        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[

       
               {"role": "system", "content": """
                        Forget everything that was said to you before. Now we will play a game with you. 
                        You are an Artificial Intelligence UI / UX Developer working in a software house and you are responsible for working on the UI / UX design of the program whose details are given to you and desired to be developed. 
                        Your most important task; to make a list for frontend developer and graphic designer by detailing the works in this task list that has been defined for you. While detailing these tasks here, you should give details to the smallest detail. 
                        Using only the information from you, frontend developers and graphic designers should be able to complete the work assigned to them. You should not provide any incomplete information. 
                        As an example, if there will be a logo in the application, what size should this logo be, 
                        what should be the file format, or if there will be another image on the page; The size, format and content of this image should be written in the most detailed way possible.
                        In the second message sent by the user, there will be general information about the project. You may need this information in your work and you have to careful to Application Tree.
                        Example answer format:
                        XXXXX FRONTEND JOBS START XXXXX
                        .
                        .....
                        .
                        XXXXX FRONTEND JOBS END XXXXX
                        XXXXX GRAPHIC DESIGN JOBS START XXXXX
                        .
                        .....
                        .
                        XXXXX GRAPHIC DESIGN JOBS END XXXXX
                                                    """},
            {"role": "user", "content": project_file_ui},
            {"role": "user", "content": Application_tree}
                ],
            temperature=1.2,
            
        )
        
 
        junior_ui_designer1 = response.choices[0].message['content'].strip()
        with open(junior1_ui_designer_file, "w", encoding="utf-8") as f:
            f.write(junior_ui_designer1)
    else:
        with open(junior1_ui_designer_file, "r", encoding="utf-8") as f:
            junior_ui_designer1 = f.read().strip()
    
    return junior_ui_designer1


def uiformater(project_name):
    # Düzenli ifade ile etiketleri tespit etme
    project_folder = os.path.join("projects", project_name)
    junior_ui_designer1 = os.path.join(project_folder, "junior1_ui_design.txt") 
    with open(junior_ui_designer1, 'r') as f:   
        junior_ui_designer1=f.read().strip()


    labels = re.findall(r'X{3,}.*?X{3,}', junior_ui_designer1)
    
    # "START" ve "END" etiketleri arasında kalan içeriği saklayalım
    sections_to_keep = []
    for i in range(0, len(labels) - 1, 2):
        start_label = labels[i]
        if i + 1 < len(labels):
            end_label = labels[i + 1]
            section_content = re.search(re.escape(start_label) + r'(.*?)' + re.escape(end_label), junior_ui_designer1, re.DOTALL)
            if section_content:
                sections_to_keep.append(section_content.group(0))
    
    refined_response = "\n".join(sections_to_keep)
    
    for label in labels:
        # Eğer label "START" veya "END" içermiyorsa bu label'ı atlayalım
        if "START" not in label and "END" not in label:
            continue
        
        start_x_count = len(re.findall(r'^X+', label)[0])
        end_x_count = len(re.findall(r'X+$', label)[0])
        
        # Eğer etiket başında veya sonunda 5'ten az "X" karakteri varsa, eksik olanları ekleyelim
        if start_x_count < 5 or end_x_count < 5:
            corrected_label = "X" * (5 - start_x_count) + label + "X" * (5 - end_x_count)
            refined_response = refined_response.replace(label, corrected_label)
    
    # "START" ve "END" arasında bir boşluk ekleyelim
    project_folder = os.path.join("projects", project_name)
    formated_junior_ui_designer1 = refined_response.replace("STARTXXXXX", "START XXXXX").replace("ENDXXXXX", "END XXXXX")
    formated_junior_ui_designer1_file = os.path.join(project_folder, "formatedui.txt")   
    if not os.path.exists(formated_junior_ui_designer1_file):
        with open(formated_junior_ui_designer1_file, "w", encoding="utf-8") as f:
            f.write(formated_junior_ui_designer1)    
    return formated_junior_ui_designer1


def ui_split_and_save(project_name):
    # Bölüm başlangıç ve bitiş tanımlamaları
    sections = {
        'XXXXX FRONTEND JOBS START XXXXX': 'frontendjobs.txt',
        'XXXXX GRAPHIC DESIGN JOBS START XXXXX': 'graphicjobs.txt'
    }
    end_sections = set([key.replace('START', 'END') for key in sections.keys()])

    # Oluşturulan dosyaların yollarını saklamak için bir liste tanımlayalım
    created_files_ui = []

    # Dosyayı okuma
    project_folder = os.path.join("projects", project_name)
    formated_ui_file = os.path.join(project_folder, "junior1_ui_design.txt") 
    with open(formated_ui_file, 'r') as file:
        lines = file.readlines()

    current_file_name = None
    for line in lines:
        stripped_line = line.strip()
        if stripped_line in sections:
            if current_file_name:
                current_file.close()
            # Dosyaları formated_project_details_file değişkeninin bulunduğu klasörde oluşturalım
            current_file_name = os.path.join(os.path.dirname(formated_ui_file), sections[stripped_line])
            created_files_ui.append(current_file_name)
            current_file = open(current_file_name, 'w')
        elif stripped_line in end_sections:
            if current_file_name:
                current_file.close()
                current_file_name = None
        elif current_file_name:
            current_file.write(line)

    if current_file_name:
        current_file.close()

    # Oluşturduğumuz dosyaların yollarını döndürelim
    return created_files_ui


def html_frontend_developer(project_name):
    project_folder = os.path.join("projects", project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    frontend_html_file = os.path.join(project_folder, "frontend_html.txt")

    
    
    frontendjobs_file = os.path.join(project_folder, "frontendjobs.txt") 
    with open(frontendjobs_file, 'r') as f:   
        frontendjobs=f.read().strip()

    frontend_file = os.path.join(project_folder, "frontend.txt") 
    with open(frontend_file, 'r') as f:   
        frontend=f.read().strip()

    Application_tree = os.path.join(project_folder, "tree.txt") 
    with open(Application_tree, 'r') as f:   
        Application_tree=f.read().strip()

    if not os.path.exists(frontend_html_file):
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[


                
              {"role": "system", "content":  """Forget everything that was said to you before. Now we will play a game with you. 
              You are an Artificial Intelligence FrontEnd Developer working in a software house and you are creating html pages in a software house. 
              Your single most important task; Using the information given to you by the UX/UI designer, coding the html pages among the tasks given to you by the user. 
              The first user message will give you the information given to you by the UX/UI designer, respectively, and the second user message has duties as the frontEnd developer department. 
              In the third message you will find the application tree that you have to comply with.
              You are the HTML CODER in this department. Remember, this is your only mission. In the message you wrote, you will only reply as html codes. 
              You can use the XXXXX bracket when you need to create more than one html page. 
               Below I leave a sample answer format for you. You have to comply with this format. Do not reply outside of this format.
               Example answer format:
               XXXXX index.html START XXXXX
               .
               .....
               .
               XXXXX index.html END XXXXX
               XXXXX page1.html START XXXXX
               .
               .....
               .
               XXXXX page1.html END XXXXX"""},
            {"role": "user", "content": frontendjobs},
            {"role": "user", "content": frontend},
            {"role": "user", "content": Application_tree}
            ],    
            temperature=0.4,
            
        )
        frontend_html_code = response.choices[0].message['content'].strip()
        with open(frontend_html_file, "w", encoding="utf-8") as f:
            f.write(frontend_html_code)
    else:
        with open(frontend_html_file, "r", encoding="utf-8") as f:
            frontend_html_code = f.read().strip()
    return frontend_html_code


def html_split_and_save_dynamic(project_name):
    # Dosyayı okuma
    project_folder = os.path.join("projects", project_name)
    frontend_file_html = os.path.join(project_folder, "frontend_html.txt") 

    # Dosyanın olup olmadığını kontrol edelim
    if not os.path.exists(frontend_file_html):
        print(f"'{frontend_file_html}' dosyası bulunamadı.")
        return []

    with open(frontend_file_html, 'r') as file:
        content = file.read()

    # Başlangıç ve bitiş etiketlerini bulma
    start_labels = re.findall(r'XXXXX (.*?) START XXXXX', content)
    
    # Oluşturulan dosyaların yollarını saklamak için bir liste tanımlayalım
    created_files_html = []

    for label in start_labels:
        # Her etiket için başlangıç ve bitiş pozisyonlarını bulma
        start_pos = content.find(f'XXXXX {label} START XXXXX')
        end_pos = content.find(f'XXXXX {label} END XXXXX')
        
        # Eğer etiketlerin her ikisi de varsa içeriği ayıklama
        if start_pos != -1 and end_pos != -1:
            extracted_content = content[start_pos + len(f'XXXXX {label} START XXXXX'):end_pos].strip()

            # Dosyaları frontend_file_html değişkeninin bulunduğu klasörde oluşturalım
            file_name = os.path.join(os.path.dirname(frontend_file_html), f'{label}')
            
            # Dosyanın bulunduğu klasörün var olup olmadığını kontrol edip, eğer yoksa bu klasörü oluşturalım
            directory = os.path.dirname(file_name)
            if not os.path.exists(directory):
                os.makedirs(directory)

            created_files_html.append(file_name)
            with open(file_name, 'w') as file:
                file.write(extracted_content)

    # Oluşturduğumuz dosyaların yollarını döndürelim
    return created_files_html


def css_frontend_developer(project_name):
    project_folder = os.path.join("projects", project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    frontend_css_file = os.path.join(project_folder, "frontend_css.txt")

    frontendjobs_file = os.path.join(project_folder, "frontendjobs.txt") 
    with open(frontendjobs_file, 'r') as f:   
        frontendjobs=f.read().strip()

    frontend_file_html = os.path.join(project_folder, "frontend_html.txt") 
    with open(frontend_file_html, 'r') as f:   
        frontend_html=f.read().strip()

    frontend_file = os.path.join(project_folder, "frontend.txt") 
    with open(frontend_file, 'r') as f:   
        frontend=f.read().strip()


    if not os.path.exists(frontend_css_file):
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[


                
              {"role": "system", "content":  """
                   You are an Artificial Intelligence FrontEnd Developer working in a software house and you are creating innovative, apple OS-like, 
                   interactive designs using pastel colors and creating css pages for the html pages given to you in a software house.
                   Your single most important task; Using the information given to you by the UX/UI designer, coding the css pages among the tasks given to you by the user.
                   In turn, the first user message will give you the information given by the UX/UI designer,
                   second user message will have html codes written for this project,
                   and the third user message will be frontEnd developer department.
                   In this section you are the CSS ENCODER. Remember, this is your only mission. You will only reply to the message you have written as html and css codes.
                   You can use XXXXX when you need to create multiple CSS pages. You can make additions and changes on the html pages given to you, provided that you do not disturb their general structure.
                   Below I leave a sample answer format for you. You must follow this format. Do not respond outside of this format.
                Example answer format:
                XXXXX style.css START XXXXX
                .
                .....
                .
                XXXXX style.css END XXXXX
                XXXXX example.css XXXXX START
                .
                .....
                .
                XXXXX example.css END XXXXX 
                XXXXX index.html START XXXXX
                .
                .....
                .
                XXXXX index.html END XXXXX
                XXXXX page1.html START XXXXX
                .
                .....
                .
                XXXXX page1.html END XXXXX          
                """
                
                },
            {"role": "user", "content": frontend},
            {"role": "user", "content": frontend_html},
            {"role": "user", "content": frontendjobs}
            ],                

            temperature=0.4,
            
        )
        frontend_css_code = response.choices[0].message['content'].strip()
        with open(frontend_css_file, "w", encoding="utf-8") as f:
            f.write(frontend_css_code)
    else:
        with open(frontend_css_file, "r", encoding="utf-8") as f:
            frontend_css_code = f.read().strip()
    return frontend_css_code

def frontend_developer_js(project_name):
    project_folder = os.path.join("projects", project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    frontend_js_file = os.path.join(project_folder, "frontend_js.txt")
    
    frontendjobs_file = os.path.join(project_folder, "frontendjobs.txt") 
    with open(frontendjobs_file, 'r') as f:   
        frontendjobs=f.read().strip()

    frontend_file_html = os.path.join(project_folder, "frontend_html.txt") 
    with open(frontend_file_html, 'r') as f:   
        frontend_html=f.read().strip()

    frontend_file = os.path.join(project_folder, "frontend.txt") 
    with open(frontend_file, 'r') as f:   
        frontend=f.read().strip()

    Application_tree = os.path.join(project_folder, "tree.txt") 
    with open(Application_tree, 'r') as f:   
        Application_tree=f.read().strip()

    if not os.path.exists(frontend_js_file):
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
                

                
              {"role": "system", "content":  """
                Forget everything you've been told before. Now we will play a game with you.
                You are an Artificial Intelligence FrontEnd Developer working in a software house and you are creating js pages in a software house.
                Your single most important task; Using the information given to you by the UX/UI designer, coding the js pages among the tasks assigned to you by the user.
                Respectively, the first user message will give you the information given by the UX/UI designer, 
                the second user message will have the html codes written for this project, 
                and the third user message will be the frontEnd developer department.
                In the forth message you will find the application tree that you have to comply with.
                In this department, you are the js ENCODER. Remember, this is your only mission. You will only reply as js codes in the message you have written.
                You can use XXXXX when you need to create multiple js pages.
                Below I leave a sample answer format for you. You must comply with this format. Do not respond outside of this format.
                Example answer format:
                XXXXX main.js START XXXXX
                .
                .....
                .
                XXXXX main.js END XXXXX
                XXXXX example.js XXXXX START
                .
                .....
                .
                XXXXX example.js END XXXXX """},
            {"role": "user", "content": frontend},
            {"role": "user", "content": frontend_html},
            {"role": "user", "content": frontendjobs},
            {"role": "user", "content": Application_tree}
            ],                

            temperature=0.2,
            
        )
        frontend_js_code = response.choices[0].message['content'].strip()
        with open(frontend_js_file, "w", encoding="utf-8") as f:
            f.write(frontend_js_code)
    else:
        with open(frontend_js_file, "r", encoding="utf-8") as f:
            frontend_js_code = f.read().strip()
    return frontend_js_code


def backend_developer(project_name):
    project_folder = os.path.join("projects", project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    backend_developer_file = os.path.join(project_folder, "backend_developer.txt")
    
    product_details_file = os.path.join(project_folder, "product_details.txt") 
    with open(product_details_file, 'r') as f:   
        product_details=f.read().strip()

    frontend_file_html = os.path.join(project_folder, "frontend_html.txt") 
    with open(frontend_file_html, 'r') as f:   
        frontend_html=f.read().strip()

    backend_file = os.path.join(project_folder, "backend.txt") 
    with open(backend_file, 'r') as f:   
        backend=f.read().strip()

    Application_tree = os.path.join(project_folder, "tree.txt") 
    with open(Application_tree, 'r') as f:   
        Application_tree=f.read().strip()

    if not os.path.exists(backend_developer_file):
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
                

                
              {"role": "system", "content":  """
Forget everything that was said to you before that. You are BackEndGPT, which is a very advanced language model. You are an artificial intelligence language model working in a software house. You are the manager of the Backend Department.
Employees in this software house have the right to communicate with each other only once. There are two artificial intelligence coders working under you in this software house. These are coder1 and Coder2 .
your duty;
Analyze the product details that the user gave in the first message and the Backend tasks that the user gave in the second message.
You will see the application tree structure in the user's third message. Here you have to create all the python files specified as .py. For this you will divide the work between Coder1 and Coder2 to create these files. 
Remember, you can only communicate with Coder1 and Coder2 once. That's why you have to write the message as detailed and descriptive as possible. They will only python the whole project with the information they get from you, so you have to be very descriptive. I leave you a sample answer format. Do not provide information outside of this format. You have to follow the format exactly. Don't forget Analyze the product details that the user gave in the first message and the Backend tasks that the user specified in the second message.
Give them the best possible detail and describe them by creating separate to-do lists for coder1 and coder2.
                        
                         Example answer format:
                         XXXXX CODER1 START XXXXX
                         .
                         .....
                         .
                         XXXXX CODER1 END XXXXX

                         XXXXX CODER2 START XXXXX
                         .
                         .....
                         .
                         XXXXX CODER2 END XXXXX """},
            {"role": "user", "content": product_details},
            {"role": "user", "content": backend},
            {"role": "user", "content": Application_tree}
            ],                

            temperature=1.4,
            
        )
        backend_developer_code = response.choices[0].message['content'].strip()
        with open(backend_developer_file, "w", encoding="utf-8") as f:
            f.write(backend_developer_code)
    else:
        with open(backend_developer_file, "r", encoding="utf-8") as f:
            backend_developer_code = f.read().strip()
    return backend_developer_code



def backend_split_and_save_dynamic(project_name):
    # Dosyayı okuma
    project_folder = os.path.join("projects", project_name)
    backend_file = os.path.join(project_folder, "backend_developer.txt") 

    # Dosyanın olup olmadığını kontrol edelim
    if not os.path.exists(backend_file):
        print(f"'{backend_file}' dosyası bulunamadı.")
        return []

    with open(backend_file, 'r') as file:
        content = file.read()

    # Başlangıç ve bitiş etiketlerini bulma
    start_labels = re.findall(r'XXXXX (.*?) START XXXXX', content)
    
    # Oluşturulan dosyaların yollarını saklamak için bir liste tanımlayalım
    created_files_backend = []

    for label in start_labels:
        # Her etiket için başlangıç ve bitiş pozisyonlarını bulma
        start_pos = content.find(f'XXXXX {label} START XXXXX')
        end_pos = content.find(f'XXXXX {label} END XXXXX')
        
        # Eğer etiketlerin her ikisi de varsa içeriği ayıklama
        if start_pos != -1 and end_pos != -1:
            extracted_content = content[start_pos + len(f'XXXXX {label} START XXXXX'):end_pos].strip()

            # Dosyaları frontend_file_html değişkeninin bulunduğu klasörde oluşturalım
            file_name = os.path.join(os.path.dirname(backend_file), f'{label}.txt')
            
            # Dosyanın bulunduğu klasörün var olup olmadığını kontrol edip, eğer yoksa bu klasörü oluşturalım
            directory = os.path.dirname(file_name)
            if not os.path.exists(directory):
                os.makedirs(directory)

            created_files_backend.append(file_name)
            with open(file_name, 'w') as file:
                file.write(extracted_content)

    # Oluşturduğumuz dosyaların yollarını döndürelim
    return created_files_backend

def get_code_blocks( project_name):
    
    project_folder = os.path.join("projects", project_name)
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)

    Application_tree = os.path.join(project_folder, "tree.txt") 
    with open(Application_tree, 'r') as f:   
        Application_tree=f.read().strip()

    backend_file = os.path.join(project_folder, "CODER1.txt") 
    with open(backend_file, 'r') as f:   
        backend=f.read().strip()   

    js_file = os.path.join(project_folder, "frontend_js.txt") 
    with open(js_file, 'r') as f:   
        js=f.read().strip()  
 
    frontend_file_html = os.path.join(project_folder, "frontend_html.txt") 
    with open(frontend_file_html, 'r') as f:   
        frontend_html=f.read().strip()       
    
    code_blocks_file = os.path.join(project_folder, "code_blocks.txt")
    if not os.path.exists(code_blocks_file):
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[

                
                {"role": "system", "content":  """           
                Forget everything you've been told before. Now we will play a game with you.
                You are an Artificial Intelligence BackEnd Developer working in a software house and you are creating python pages in a software house.
                Your single most important task; Coding python pages among user-assigned tasks using the information given to you by the Project Manager.
                In order, 
                In the first message you will find the application tree that you have to comply with. You have to create the contents of all the .py files that exist in the application tree.
                the second user message will give you the information given by the Project Manager, 
                the third user message will give the html codes written for this project, 
                the forth user message will give the js codes written for this project.
                Remember, this is your mission. You have to write the codes that will work fully and completely with the information given to you. 
                Do not leave any function in any file as blank or comment. 
                You have to fill them all. All transactions must be carried out in accordance with the tasks assigned to you.
                In this department, you are your PYTHON CODE PRINTER. Remember, this is your only mission. In the message you have written, you will only reply as PYTHON codes.
                You can use XXXXX when you need to create multiple PYTHON pages.
                 Below I leave a sample answer format for you. You must comply with this format. Do not respond outside of this format.
                 It's about giving a single answer. That's why I want you to write as detailed and complete as possible. Before writing an answer, check your answer, correct it if there are any missing, then write the answer. 
                 There's no going back. The only answer you give is to create all the .py files requested from you in the production tree.
                 Example answer format:
                 XXXXX app.py START XXXXX
                 .
                 .....
                 .
                 XXXXX app.py END XXXXX

                 XXXXX __init__.py START XXXXX 
                 .
                 .....
                 .
                 XXXXX __init__.py END XXXXX

                 XXXXX user.py START XXXXX 
                 .
                 .....
                 .
                 XXXXX user.py END XXXXX """},
                {"role": "user", "content": Application_tree},
                {"role": "user", "content": backend},
                {"role": "user", "content": frontend_html},
                {"role": "user", "content": js}
            ],
            temperature=0.2,
            
        )
        code_blocks = response.choices[0].message['content'].strip()

        with open(code_blocks_file, "w" , encoding="utf-8") as f:
            f.write(code_blocks)
    else:
        with open(code_blocks_file, "r" , encoding="utf-8") as f:
            code_blocks = f.read().strip()

    return code_blocks


def py_split_and_save_dynamic(project_name):
    # Dosyayı okuma
    project_folder = os.path.join("projects", project_name)
    code_blocks_file = os.path.join(project_folder, "code_blocks.txt") 
    with open(code_blocks_file, 'r') as f:   
        code_blocks=f.read().strip() 
    # Dosyanın olup olmadığını kontrol edelim
    if not os.path.exists(code_blocks_file):
        print(f"'{code_blocks}' dosyası bulunamadı.")
        return []

    with open(code_blocks_file, 'r') as file:
        content = file.read()

    # Başlangıç ve bitiş etiketlerini bulma
    start_labels = re.findall(r'XXXXX (.*?) START XXXXX', content)
    
    # Oluşturulan dosyaların yollarını saklamak için bir liste tanımlayalım
    created_files_py = []

    for label in start_labels:
        # Her etiket için başlangıç ve bitiş pozisyonlarını bulma
        start_pos = content.find(f'XXXXX {label} START XXXXX')
        end_pos = content.find(f'XXXXX {label} END XXXXX')
        
        # Eğer etiketlerin her ikisi de varsa içeriği ayıklama
        if start_pos != -1 and end_pos != -1:
            extracted_content = content[start_pos + len(f'XXXXX {label} START XXXXX'):end_pos].strip()

            # Dosyaları frontend_file_html değişkeninin bulunduğu klasörde oluşturalım
            file_name = os.path.join(os.path.dirname(code_blocks_file), f'{label}')
            
            # Dosyanın bulunduğu klasörün var olup olmadığını kontrol edip, eğer yoksa bu klasörü oluşturalım
            directory = os.path.dirname(file_name)
            if not os.path.exists(directory):
                os.makedirs(directory)

            created_files_py.append(file_name)
            with open(file_name, 'w') as file:
                file.write(extracted_content)

    # Oluşturduğumuz dosyaların yollarını döndürelim
    return created_files_py



@app.route("/", methods=["GET", "POST"])
def index():


    if request.method == "POST":
        project_name = request.form["project_name"]
        project_description = request.form["project_description"]
        technologies = request.form["technologies"]
        product_details=product_manager(project_name, project_description, technologies)
        project_details = project_manager(project_name)
        formated_project_details = pmformater(project_name)
        created_files_pm = pm_split_and_save(project_name)
        junior_ui_designer1 = junior1_ui_designer(project_name)
        formated_junior_ui_designer1 = uiformater(project_name)
        created_files_ui = ui_split_and_save(project_name)
        frontend_html_code = html_frontend_developer(project_name)
        created_files_html = html_split_and_save_dynamic(project_name)
        frontend_css_code = css_frontend_developer(project_name)
        frontend_js_code = frontend_developer_js(project_name)
        backend_developer_code = backend_developer(project_name)
        created_files_backend = backend_split_and_save_dynamic(project_name)
        code_blocks = get_code_blocks( project_name)
        created_files_py = py_split_and_save_dynamic(project_name)
        return render_template("project.html",project_name=project_name, project_description=project_description,technologies=technologies,product_details=product_details, project_details=project_details, code_blocks=code_blocks)
        
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)


