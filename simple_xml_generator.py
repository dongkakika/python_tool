from xml.etree.ElementTree import Element, SubElement, ElementTree, dump
import os


# Indent function 정의
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class vType():
    # 클래스 변수 선언 후 메소드를 나중에 호출하기 위해, 선언 시 바로 초기화해야 하는 __init__ 말고 init로 변경해서 메소드 정의
    def init(self, id, speed, tau, accel, decel, type, vClass):
        self.id = id
        self.speed = speed
        self.tau = tau
        self.accel = accel
        self.decel = decel
        self.type = type
        self.vClass = vClass

def makeDefaultType():
    # 함수가 끝난 뒤에 변경 내용이 사라지지 않도록 전역변수 사용 선언
    global krauss_default, kraussPS_default, ACC_default, CACC_default
    global vType_list
    krauss_default.init('Krauss', 30, 1.64, 3, 5, static_type[0], static_vClass[0])
    vType_list.append(krauss_default)
    kraussPS_default.init('KraussPS', 30, 1.64, 3, 5, static_type[1], static_vClass[0])
    vType_list.append(kraussPS_default)
    ACC_default.init('ACC', 30, 1.54, 3, 5, static_type[2], static_vClass[0])
    vType_list.append(ACC_default)
    CACC_default.init('CACC', 30, 0.71, 3, 5, static_type[3], static_vClass[0])
    vType_list.append(CACC_default)

def makeXML(vType_list):
    
    # (root1) 루트가 될 routes 태그 생성
    routes_root = Element('routes')
    # 아래는 별개로 속성 추가 방식
    routes_root.attrib["from"] = "두둥탁"

    # vType의 태그 이름을 가진 노드를 생성
    node1= Element('vType', id=vType_list[0].id, length="5.0", minGap="2.0", maxSpeed=str(vType_list[0].speed), vClass=vType_list[0].vClass)
    # node1의 자식 노드로 'carFollowing-...'을 생성
    SubElement(node1, 'carFollowing-Krauss', accel=str(vType_list[0].accel), decel=str(vType_list[0].decel), sigma="0", tau=str(vType_list[0].tau))
    # 완성된 트리 node1을 root의 자식 노드(트리)로 결합 
    routes_root.append(node1)

    # 이하 동일 과정
    node2 = Element('vType', id=vType_list[1].id, length="5.0", minGap="2.0", maxSpeed=str(vType_list[0].speed), vClass=vType_list[0].vClass)
    node2.attrib["from"]= "adding attribute!"
    SubElement(node2, 'carFollowing-Krauss', accel=str(vType_list[1].accel), decel=str(vType_list[1].decel), sigma="0", tau=str(vType_list[1].tau))
    routes_root.append(node2)

    node3 = Element('vType', id=vType_list[2].id, length="5.0", minGap="2.0", maxSpeed=str(vType_list[0].speed), vClass=vType_list[0].vClass)
    SubElement(node3, 'carFollowing-Krauss', accel=str(vType_list[2].accel), decel=str(vType_list[2].decel), tau=str(vType_list[2].tau), controllerDelay="0.5", ComfAccel="3.0", ComfDecel="5.0", K_sc="0.4", K_v="1.0", K_g="5.0", V_int="30.0")
    routes_root.append(node3)

    node4 = Element('vType', id=vType_list[3].id, length="5.0", minGap="2.0", maxSpeed=str(vType_list[0].speed), vClass=vType_list[0].vClass)
    SubElement(node4, 'carFollowing-Krauss', accel=str(vType_list[3].accel), decel=str(vType_list[3].decel), tau=str(vType_list[3].tau), controllerDelay="0.5", ComfAccel="3.0", ComfDecel="5.0", K_sc="0.4", K_v="0.99", K_g="4.08", K_a="0.66", V_int="30.0", degradeToACC="0", invalidTimer="0.1")
    routes_root.append(node4)



    # (root2) 루트가 될 configuration 태그 생성
    conf_root = Element('configuration', temp="language")
    
    # time의 태그 이름을 가진 노드를 생성
    time_node = Element('time')
    # time_node의 자식 노드로 'begin', 'end', 'step-length'을 생성
    SubElement(time_node, 'begin', value=str("0"))
    SubElement(time_node, 'end', value=str("-1"))
    SubElement(time_node, 'step-length', value=str("0.1"))
     # 완성된 트리 time_node를 root의 자식 노드(트리)로 결합
    conf_root.append(time_node)

    # processing의 태그 이름을 가진 노드를 생성
    processing_node = Element('processing')
    SubElement(processing_node, 'time-to-teleport', value=str("0"))
    SubElement(processing_node, 'xml-validation', value=str("never"))
    conf_root.append(processing_node)

    # report의 태그 이름을 가진 노드를 생성
    report_node = Element('report')
    SubElement(report_node, 'verbose', value='true')
    conf_root.append(report_node)
    
    # 줄 바꿈, 열 맞추기를 실시하는 indent 함수 사용, 파라미터는 루트 노드
    indent(routes_root)
    indent(conf_root)

    # 인터프리터 쉘에서 결과 확인하기 위한 dump 함수 사용
    #dump(routes_root, conf_root)

    # 두 root1, root2를 합치기 위해 각 xml 파일 생성
    # 1. routes xml을 생성
    tree = ElementTree(routes_root)
    filename = "routes" 
    tree.write('./' + filename + ".xml", encoding="utf-8", xml_declaration=True)

    # 2. configuration xml을 생성
    tree = ElementTree(conf_root)
    filename = "conf"
    tree.write('./' + filename + ".xml", encoding="utf-8", xml_declaration=True)

    # routes.xml 파일에 conf.xml 파일을 덮어쓰기
    f1 = open('routes.xml', 'a')
    f2 = open('conf.xml', 'r')
    count = 1
    while True:
        line = f2.readline()
        if(count == 1):
            count += 1
            continue
        if not line: break
        f1.write(line)
        
    f2.close()
    f1.close()

    # 중간에 생성된 conf.xml 삭제
    os.remove('conf.xml')
    
    
### MAIN

# Global 변수 선언
krauss_default = vType()
kraussPS_default = vType()
ACC_default = vType()
CACC_default = vType()
vType_list = []

static_type = ['Krauss', 'KraussPS', 'ACC', 'CACC']
static_vClass = ['passenger', 'bus']

makeDefaultType()
makeXML(vType_list)


