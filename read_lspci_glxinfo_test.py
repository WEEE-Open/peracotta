from read_lspci_and_glxinfo import read_lspci_and_glxinfo

"""START TEST"""
glxinfo_path = ""
lspci_path = ""
has_dedicated = None

# dedicated:
_2018mbp = 0
_2014mbp = 0
castes_pc = 0
_9400gt = 0
gtx970 = 0
asdpc = 0
castes_HP_G100 = 0
_6200 = 0

# integrated:
# jm11 = 0
_8300gt = 0
_82865g = 0
es1000 = 0
castes_HP_82945G = 1
acer_swift3 = 0
HP_elitebook_2540p = 0
xeon = 0

# dedicated:
if _2018mbp:
    glxinfo_path = "2018-castes-mbp/glxinfo.txt"
    lspci_path = "2018-castes-mbp/lspci.txt"
    has_dedicated = True
elif _2014mbp:
    glxinfo_path = "2014-castes-mbp/glxinfo.txt"
    lspci_path = "2014-castes-mbp/lspci.txt"
    has_dedicated = True
elif castes_pc:
    glxinfo_path = "castes-pc/glxinfo.txt"
    lspci_path = "castes-pc/lspci.txt"
    has_dedicated = True
elif _9400gt:
    glxinfo_path = "glxinfo+lspci/dedicated/glxinfo-9400GT.txt"
    lspci_path = "glxinfo+lspci/dedicated/lspci-9400GT.txt"
    has_dedicated = True
elif gtx970:
    glxinfo_path = "glxinfo+lspci/dedicated/glxinfo-gtx-970.txt"
    lspci_path = "glxinfo+lspci/dedicated/lspci-gtx-970.txt"
    has_dedicated = True
elif asdpc:
    glxinfo_path = "asdpc/glxinfo.txt"
    lspci_path = "asdpc/lspci.txt"
    has_dedicated = True
elif castes_HP_G100:
    glxinfo_path = "castes-HP-dc7600/NVIDIA-G100/glxinfo.txt"
    lspci_path = "castes-HP-dc7600/NVIDIA-G100/lspci.txt"
    has_dedicated = True
elif _6200:
    glxinfo_path = "glxinfo+lspci/dedicated/NVIDIA6200/glxinfo.txt"
    lspci_path = "glxinfo+lspci/dedicated/NVIDIA6200/lspci.txt"
    has_dedicated = True

# integrated:
# elif jm11:
#     glxinfo_path = "castes-pc/glxinfo.txt"
#     lspci_path = "castes-pc/lspci.txt"
elif _8300gt:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-8300GT.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-8300GT.txt"
    has_dedicated = False
elif _82865g:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-82865G.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-82865G.txt"
    has_dedicated = False
elif es1000:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-ES1000.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-ES1000.txt"
    has_dedicated = False
elif castes_HP_82945G:
    glxinfo_path = "castes-HP-dc7600/82945G/glxinfo.txt"
    lspci_path = "castes-HP-dc7600/82945G/lspci.txt"
    has_dedicated = False
elif acer_swift3:
    glxinfo_path = "glxinfo+lspci/integrated/on-cpu/Acer Swift 3/glxinfo.txt"
    lspci_path = "glxinfo+lspci/integrated/on-cpu/Acer Swift 3/lspci.txt"
    has_dedicated = False
elif HP_elitebook_2540p:
    glxinfo_path = "glxinfo+lspci/integrated/on-cpu/HP EliteBook 2540p (i5 M540)/glxinfo.txt"
    lspci_path = "glxinfo+lspci/integrated/on-cpu/HP EliteBook 2540p (i5 M540)/lspci.txt"
    has_dedicated = False
elif xeon:
    glxinfo_path = "glxinfo+lspci/integrated/on-cpu/Xeon/glxinfo.txt"
    lspci_path = "glxinfo+lspci/integrated/on-cpu/Xeon/lspci.txt"
    has_dedicated = False
"""END TEST"""

read_lspci_and_glxinfo(has_dedicated, lspci_path, glxinfo_path)