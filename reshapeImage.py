from PIL import Image  
import os  
  
# 设置图片所在的文件夹路径  
folder_path = './data/test'
  
# 遍历文件夹中的所有文件  
for filename in os.listdir(folder_path):  
    # 忽略非图片文件  
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):  
        continue  
      
    # 构造图片文件的完整路径  
    file_path = os.path.join(folder_path, filename)  
      
    try:  
        # 打开图片  
        img = Image.open(file_path)  
          
        # 调整图片大小到120x40，注意保持图片的纵横比可能会导致图片变形  
        # 如果你想要裁剪图片以填充整个120x40的区域，你可以使用thumbnail或resize后裁剪  
        # 这里我们使用resize并忽略纵横比  
        resized_img = img.resize((120, 40))  
          
        # 保存调整大小后的图片，可以选择是否覆盖原图片  
        # 这里我们选择保存为新的文件名，避免覆盖原文件  
        base, ext = os.path.splitext(filename)  
        resized_file_path = os.path.join(folder_path, base  + ext)  
        resized_img.save(resized_file_path)  
          
        print(f'Resized {filename} to {resized_file_path}')  
    except IOError as e:  
        print(f'Error resizing {filename}: {e.strerror}')