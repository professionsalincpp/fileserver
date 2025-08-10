from cx_Freeze import setup, Executable

path = ["src"]
dep = [  "config",
         "logger",
         "request_handler", 
         "utils.path", 
         "policyservices.policyworker", 
         "policyservices.policyworkermode", 
         "policyservices.policyworkerstatus", 
         "policyservices.policyworkerresult", 
         "handlers.response", "handlers.GEThandler", 
         "handlers.POSThandler", "handlers.POSTChecker", 
         "fileservices.fileworker", "fileservices.fileworkermode", 
         "fileservices.fileworkerstatus", "fileservices.fileworkerresult",
         ]
# for i in range(len(dep)):
#     dep[i] = "src." + dep[i]

build_exe_options = {
    "includes": dep,
    "build_exe": "..\\bin\\v1.0.4"
}

setup(
    name="Мой сервер",
    version="1.0",
    description="Мой сервер",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")],
)