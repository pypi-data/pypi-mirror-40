# person_company_name_classification

加载训练好的模型，进行预测


要想直接使用预测模块，可通过 pip install predict-cl-name 
predict-cl-name.predict_name(字符串)





整个项目使用步骤如下：

模型训练的过程:
1, 解压settings/filepath/data_name.tar.xz
2, pip install -r requirements.txt
3, 如果想改变读取数据量，请改变settings下get_train_data.py里self.n的值,  读取全部数据请把while i < self.n:  改成 while True:
4, 如果想改变训练的数据量,请改变settings下split_data_with_label()里sn的值
5, 运行merge.py即可训练模型
6,与predict-cl-name同级新建xxx.py文件即可测试
import predict_person_company_name
print(predict_person_company_name.predict("安徽枞合农业专业合作社"))   # 测试


预测模块的使用:
1, pip install -r requirements.txt,  requirements.txt在docs下面
2, import predict_person_company_name   
print(predict_person_company_name.predict_name("addle"))

3、项目克隆地址：git@gitlab.kingdomai.com:wangqiang/person_company_name_classification.git

4、代码在master/dev/wangqiang 分支





