import os
import win32com.client

BASE_DIR = "C:/Users/crazy/Dropbox"

# hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
# hwp.RegisterModule('FilePathCheckDLL','FilePathCheckerModule')
# hwp.Open(os.path.join(BASE_DIR, "이수구분 정정 신청서.hwp"))
# hwp.SaveAs(os.path.join(BASE_DIR,"이수구분 정정 신청서.pdf"), "PDF")
# hwp.Quit()

# powerpoint = win32com.client.gencache.EnsureDispatch("Powerpoint.Application")
powerpoint = win32com.client.gencache.EnsureDispatch("Powerpoint.Application")
ppt = powerpoint.Presentations.Open("C:/Users/crazy/Dropbox/수업/19-1_산학협력프로젝트1/산협프 발표.pptx",-1)
# ppt = powerpoint.Presentations.Open("C:/Users/crazy/Dropbox/수업/19-2_산학협력프로젝트2/5주차_미팅내용.pptx",-1)
# ppt.PrintOut(PrintToFile="C:/Users/crazy/Dropbox/수업/19-2_산학협력프로젝트2/5주차_미팅내용.pdf")