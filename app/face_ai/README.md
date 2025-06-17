# README #


### Face recognition installation###

* download python 3.7
* python libraries for ubuntu: pip install cmake==3.22.6 dlib==19.24.0 face_recognition==1.3.0 pillow==7.1.2 numpy==1.21.6 IPython==8.4.0 deepface==0.0.75 imutils==0.5.4
* python libraries for windows: pip install cmake==3.22.6 dlib==19.24.0 face_recognition==1.3.0 pillow==7.1.2 numpy==1.21.6 IPython==7.34.0 deepface==0.0.75 imutils==0.5.4
* how to run: you should add 3 arguments: mode, image_path, and id(if required)
* $python3 recognition.py --mode new --image_path img.jpg --id 123 (this example to add new face and id)
* $python3 recognition.py --mode detect --image_path img.jpg (this example to detect current face)


* python libraries: 
pip install pillow==7.1.2 
pip install numpy==1.21.6
pip install face_recognition==1.3.0 
pip install cmake==3.22.6
pip install dlib==19.24.0
pip install IPython==8.4.0 # pip install IPython==7.34.0 # For Windows
pip install deepface==0.0.75
pip install imutils==0.5.4


* run
$ python3.8 recognition.py --mode new --image_path images/1.jpeg --id 100001 --cpu 2 --id_folder id_folder
$ python3.8 recognition.py --mode detect --image_path images/1.jpeg --tol 0.7 --cpu 4 --id_folder id_folder
$ python3.8 recognition.py --mode del --id 100001 --id_folder id_folder


* test
$ python3.8 recognition.py --image_path images/1.jpeg --id 100001 --cpu 2 --id_folder ./id_folder
$ python3.8 recognition.py --mode new --id 100001 --cpu 2 --id_folder ./id_folder
$ python3.8 recognition.py --mode new --image_path images/1.jpeg --cpu 2 --id_folder ./id_folder
$ python3.8 recognition.py --mode new --image_path images/1.jpeg --id 100001 --id_folder ./id_folder
$ python3.8 recognition.py --mode new --image_path images/1.jpeg --id 100001 --cpu 2

$ python3.8 recognition.py --image_path images/1.jpeg --tol 0.7 --cpu 4 --id_folder ./id_folder
$ python3.8 recognition.py --mode detect --tol 0.7 --cpu 4 --id_folder ./id_folder
$ python3.8 recognition.py --mode detect --image_path images/1.jpeg --cpu 4 --id_folder ./id_folder
$ python3.8 recognition.py --mode detect --image_path images/1.jpeg --tol 0.7 --id_folder ./id_folder
$ python3.8 recognition.py --mode detect --image_path images/1.jpeg --tol 0.7 --cpu 4 

$ python3.8 recognition.py --mode new --image_path images/1.jpeg --id 100001 --cpu 2 --id_folder ./id_folder
$ python3.8 recognition.py --mode new --image_path images/t_2.jpeg --id 100002 --cpu 2 --id_folder ./id_folder
$ python3.8 recognition.py --mode new --image_path images/3.jpeg --id 100003 --cpu 2 --id_folder ./id_folder
$ python3.8 recognition.py --mode detect --image_path images/1.jpeg --tol 0.7 --cpu 4 --id_folder ./id_folder
$ python3.8 recognition.py --mode detect --image_path images/t5.png --tol 0.7 --cpu 4 --id_folder ./id_folder
$ python3.8 recognition.py --mode detect --image_path images/t6.png --tol 0.7 --cpu 4 --id_folder ./id_folder
$ python3.8 recognition.py --mode detect --image_path images/t_2.jpeg --tol 0.7 --cpu 4 --id_folder ./id_folder
$ python3.8 recognition.py --mode del --id 100001 --id_folder id_folder


python3.8 recognition.py --mode detect --image_path images/1.jpeg --tol 0.7 --cpu 4 --id_folder ./id_folder


* face_recognition
https://github.com/ageitgey/face_recognition
https://pypi.org/project/face-recognition/


* How to install dlib v19.9
https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf 


* warning list:
"warning": "the defualt number of CPU will use"

* error list:
"err": "id id_num already not in our database"
"err": "please provide the mode"
"err": "please provide the id"
"err": "please provide the image path"
"err": "please add tol argument"

* ok list:
"ok": "face and ID save"



مطلوب اضافة متغيرات عند تشغيل python
	1 - tolerance :: (الافتراضي 0.6) للتحكم بمستوى الدقة
	2 - cpus :: للتحكم بعدد CPUs لغرض التسريع
	
	
مطلوب اضافة البيانات التالية في output
	- لو تم رصد اكثر من شخص في نفس الصورة , مطلوب ارجاع المعلومات
	- طريقة ارجاع البيانات في صيغة  json
	- لو لم يتم تعرف للوجه في الصورة لا يعيد شئ مطلوب تجهيز رسالة مناسبة داخل JSON (يمكن اعطاءه صورة سوداء فارغة)
	- عرض نسبة الثقة بنتيجة التعرف
	- حالة الوجه (مبتسم , عادي , ....)
	- الجنس (ان امكن)
	- العمر (ان امكن)
	- لون البشرة (ان امكن)

مطلوب عند تشغيل  recognition.py
	- لو فرضنا انه لم يتم ادخال اي متغير , مطلوب ارجاع كافة الاخطاء داخل json
	- تجهيز قائمة بجميع انواع الاخطاء التي ممكن ان تظهر
	
	
	
	
	
* ملاحظات اليوم
1 - النتائج يجب ان تكون على صيغة JSON داخل Log وليس في ملف منفصل
2 - ارجاع قيمة tolerance داخل json
3 - عند اعطاءه صورة سوداء كانت النتائج [] :: من المتوقع عرض unknown
4 - لم يتم استخدام المتغير image-path ولم يظهر الخطأ داخل JSON :: من المتوقع ظهور اي خطأ داخل JSON
5 - مطلوب اضافة خدمة حذف شخص من التدريب (الهدف منها التراجع عن تدريب خاطئ)
6 - اضافة متغير جديد لتحديد مكان id_folder

* أسئلة 
- هل يمكن عمل adapt اكثر لنفس المستخدم (لانه يتم استخدام id) ? 
- في حال عمل adapt لصورة تحتوي على اكثر من شخص وباسم واحد ماذا يحصل ? 





















 * 17 Aug

 1 - اضافة متغير جديد لتحديد مكان id_folder والسبب عن تشغيله عن طريق nodejs يظهر هذا الخطأ
 2 - ارجاع قيمة tolerance من نوع double داخل json
 3 - هذه الصيغة ليست jSON تنقصها double citation
	 {"err": id 100001 already not in our database"}
	 {"ok": id 100001 removed"}

 
 4 -  عند تشغيل recognition.py يجب ان تكون النتيجة على شكل json واحد فقط يحتوي على كافة الانواع ان وجدت 
 - مثال على الصيغة المطلوبة
 {
 "warning":"",
 "err":"" ,
 "ok": "",
 data: [{"id": "100001", "accuracy": 85.185, "tolerance": 0.7},{"id": "100001", "accuracy": 85.185, "tolerance": 0.7}]
 }
 
 5- عند اعطائة صورة سوداء مطلوب JSON كما يلي
 {data:[{"id": "Unknown"}]}
 
 
 6- مطلوب تزويدي بقائمة الاخطاء التي ممكن ان تتحدث




* أسئلة 
- هل يمكن عمل adapt اكثر لنفس المستخدم (لانه يتم استخدام id) ? 
- في حال عمل adapt لصورة تحتوي على اكثر من شخص وباسم واحد ماذا يحصل ? 




* 21 Aug


1- عند تشغيل python مطلوب حذف log والحفاظ على JSON فقط 
	- يوجد نص خارج json سيمنع من تحليل النتائج
2- عند تشغيل detect
	- بدأ بتحميل (facial_expression_model_weights.h5 , age_model_weights.h5 , gender_model_weights.h5 , race_model_single_batch.h5)
	- لكنه لم ينتهي من التحميل وظهر الخطأ  ValueError: ('Confirm that ', 'jp2.jpg', ' exists')
	- وبعد حلها من قبل المهندس رامي وعمل pull ظهر خطأ جديد
	ValueError: attempt to get argmin of an empty sequence
	- وبعد ذلك لم يظهر هذا الخطأ

3-  عند تشغيل  detect :: مطلوب الغاء log  والحفاظ على JSON فقط
 1/1 [==============================] - 0s 336ms/step
 
4- عند التعرف على صورة تحتوي على شخصين يظهر age , gender خارج json وايضا قيمة واحدة غير معروفة لاي شخص

5- JSOn هنا خاطئ {data: [{"id": "Unknown"}]}
- data تحتاج الى double citation

6 - في احد النتائج ظهر مستخدم Unknown وكانت accuracy 84 
	- هذا بسبب خطأ في التدريب (تدريب نفس الصورة بمعرف مختلف)
	- هنا مطلوب الغاء هذه النتيجة
 




30 Aug
- عند التدريب على صورة معينة  , البرنامج لا يتمكن من اعادة التعرف عليها
	- نسخة اليوم لم تتمكن من التعرف على اي شخص
	- لذلك لن اتمكن من فحص (الجنس , العمر , الاسم)
- عند تشغيل التعرف ما زال يظهر ب log اسطر debuge نحن لسنا بحاجتها
1/1  [==============================] - 0s 302ms/step
1/1  [==============================] - 0s 270ms/step
- عند عدم مقدرته على التعرف لا يظهر Unknown بل نتيجة فارغة {"data": []}
	- المتوقع {data: [{"id": "Unknown"}]}

- عند تشغيل التعرف واعطائه صورة مكانها خطأ فقع البرنامج مطلوب استخدام try .. catch

