#!/usr/bin/python2

# -*- coding: utf-8 -*-
__author__ = 'ubaldino'
__copyright__ = "...."

from optparse import OptionParser
from serial.tools import list_ports
import wx, os, time, serial , threading , re

class Validate_Numeric(wx.PyValidator):
    def __init__(Self):
        wx.PyValidator.__init__(Self)
        Self.Bind(wx.EVT_TEXT, Self.On_Text_Change)

    def Clone(Self):
        return Validate_Numeric()

    def On_Text_Change(Self, Event):
        TextCtrl = Self.GetWindow()
        Text = TextCtrl.GetValue()
        if Text.isdigit():
            TextCtrl.SetBackgroundColour("White")
        else:
            TextCtrl.SetBackgroundColour("Red")
        Event.Skip()

class Validate_Numeric_Port(wx.PyValidator):
    def __init__(Self):
        wx.PyValidator.__init__(Self)
        Self.Bind(wx.EVT_TEXT, Self.On_Text_Change)

    def Clone(Self):
        return Validate_Numeric_Port()

    def On_Text_Change(Self, Event):
        TextCtrl = Self.GetWindow()
        Text = TextCtrl.GetValue()
        if ( Text.isdigit() ) and len(Text) < 5:
            TextCtrl.SetBackgroundColour("White")
        else:
            TextCtrl.SetBackgroundColour("Red")
        Event.Skip()


class Validate_Numeric_Dot(wx.PyValidator):
    def __init__(Self):
        wx.PyValidator.__init__(Self)
        Self.Bind(wx.EVT_TEXT, Self.On_Text_Change)

    def Clone(Self):
        return Validate_Numeric_Dot()

    def Validate(self, win):
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def On_Text_Change(Self, Event):
        a = re.compile("^[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}$")
        TextCtrl = Self.GetWindow()
        Text = TextCtrl.GetValue()
        if a.match(Text):
            TextCtrl.SetBackgroundColour( wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW) )
            TextCtrl.SetFocus()
            TextCtrl.Refresh()
        else:
            TextCtrl.SetBackgroundColour("Red")
            TextCtrl.SetFocus()
            TextCtrl.Refresh()
        Event.Skip()


class Validate_Text(wx.PyValidator):
    def __init__(Self):
        wx.PyValidator.__init__(Self)
        Self.Bind(wx.EVT_TEXT, Self.On_Text_Change)

    def Clone(Self):
        return Validate_Text()

    def On_Text_Change(Self, Event):
        TextCtrl = Self.GetWindow()
        Text = TextCtrl.GetValue()
        if not Text.isdigit():
            TextCtrl.SetBackgroundColour("White")
        else:
            TextCtrl.SetBackgroundColour("Pink")
        Event.Skip()


class Main(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Sawers 1.0', size=( 650, 600 ))
        self.icon = wx.Icon(os.path.join(os.getcwd(), "resources", "sawers.ico"), wx.BITMAP_TYPE_ICO)
        #"Control",
        self.SetIcon(self.icon)
        self.panel = wx.Panel(self, -1)
        self.count_conect = 0
        self.puerto_serial = None

        self.btn_buscar = wx.Button(self.panel, label='Buscar', pos=( 30, 520 ))
        self.btn_conectar = wx.Button(self.panel, label='Conectar', pos=( 430, 520 ))
        self.btn_desconectar = wx.Button(self.panel, label='Desconectar', pos=( 525, 520 ))
        self.btn_verificar = wx.Button(self.panel, label='Verificar', pos=( 30, 200 ))

        #### Text fomularios ######
		## cambiar de ip
        self.btn_ip = wx.Button(self.panel, label='Ip', pos=( 150, 40 ))
        self.lbl_ip = wx.StaticText(self.panel, label="DIRECCION IP", pos=( 80, 20 ))
        self.txt_ip = wx.TextCtrl(self.panel, value="192.168.1.1", style=wx.TE_CENTRE, pos=( 30, 40 ), size=(110, 25), validator=Validate_Numeric_Dot())


        self.btn_puerto = wx.Button(self.panel, label='Puerto', pos=( 148, 100 ))
        self.lbl_puerto = wx.StaticText(self.panel, label="PUERTO", pos=( 80, 80 ))
        self.txt_puerto = wx.TextCtrl(self.panel, value="80", style=wx.TE_CENTRE, pos=( 30, 100 ), size=(110, 25),
                                      validator=Validate_Numeric_Port())
        #self.txt_ip.setFocus()

        self.select_device = wx.ComboBox(self.panel, pos=( 30, 150 ), size=( 95, -1), style=wx.CB_READONLY)
        self.lista_devices = {0 : 'NINGUNO' , 29:'MAESTRO' }
        for i in range(30):
            self.lista_devices[i+30] = "ESCLAVO %s"%(i+1)
        print self.lista_devices
        self.select_device.SetItems( self.lista_devices.values() )
        self.select_device.SetSelection(0)


        #  outs
        self.lbl_hexs = wx.StaticText(self.panel, label="HEX", pos=( 340, 20 ))
        self.txt_hex1 = wx.TextCtrl(self.panel, value=str(hex(1)), style=wx.TE_CENTRE, pos=( 310, 40 ), size=(100, 25))
        self.txt_hex2 = wx.TextCtrl(self.panel, value=str(hex(2)), style=wx.TE_CENTRE, pos=( 310, 70 ), size=(100, 25))
        self.txt_hex3 = wx.TextCtrl(self.panel, value=str(hex(3)), style=wx.TE_CENTRE, pos=( 310, 100 ), size=(100, 25))
        self.txt_hex4 = wx.TextCtrl(self.panel, value=str(hex(4)), style=wx.TE_CENTRE, pos=( 310, 130 ), size=(100, 25))
        self.txt_hex5 = wx.TextCtrl(self.panel, value=str(hex(5)), style=wx.TE_CENTRE, pos=( 310, 160 ), size=(100, 25))
        self.txt_hex6 = wx.TextCtrl(self.panel, value=str(hex(6)), style=wx.TE_CENTRE, pos=( 310, 190 ), size=(100, 25))

        self.lbl_outs = wx.StaticText(self.panel, label="COMANDO", pos=( 425, 20 ))
        self.txt_out1 = wx.TextCtrl(self.panel, value="80", style=wx.TE_CENTRE, pos=( 430, 40 ), size=(80, 25),
                                      validator=Validate_Numeric_Port())
        self.txt_out2 = wx.TextCtrl(self.panel, value="80", style=wx.TE_CENTRE, pos=( 430, 70 ), size=(80, 25),
                                      validator=Validate_Numeric_Port())
        self.txt_out3 = wx.TextCtrl(self.panel, value="80", style=wx.TE_CENTRE, pos=( 430, 100 ), size=(80, 25),
                                      validator=Validate_Numeric_Port())
        self.txt_out4 = wx.TextCtrl(self.panel, value="80", style=wx.TE_CENTRE, pos=( 430, 130 ), size=(80, 25),
                                      validator=Validate_Numeric_Port())
        self.txt_out5 = wx.TextCtrl(self.panel, value="80", style=wx.TE_CENTRE, pos=( 430, 160 ), size=(80, 25),
                                      validator=Validate_Numeric_Port())
        self.txt_out6 = wx.TextCtrl(self.panel, value="80", style=wx.TE_CENTRE, pos=( 430, 190 ), size=(80, 25),
                                      validator=Validate_Numeric_Port())

        self.btn_out1 = wx.Button(self.panel, label='OUT 1', pos=( 520, 40 ))
        self.btn_out2 = wx.Button(self.panel, label='OUT 2', pos=( 520, 70 ))
        self.btn_out3 = wx.Button(self.panel, label='OUT 3', pos=( 520, 100 ))
        self.btn_out4 = wx.Button(self.panel, label='OUT 4', pos=( 520, 130 ))
        self.btn_out5 = wx.Button(self.panel, label='OUT 5', pos=( 520, 160 ))
        self.btn_out6 = wx.Button(self.panel, label='OUT 6', pos=( 520, 190 ))

        #### End Text fomularios ######

        #### Eventos botones ######
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.buscar_seriales)
        self.btn_conectar.Bind(wx.EVT_BUTTON, self.conectar_dispositivo)
        self.btn_desconectar.Bind(wx.EVT_BUTTON, self.desconectar_dispositivo)
        self.btn_verificar.Bind(wx.EVT_BUTTON, self.verificar_dispositivo)

        self.btn_ip.Bind(wx.EVT_BUTTON, self.evento_ip )
        self.btn_puerto.Bind(wx.EVT_BUTTON, self.evento_puerto )

        self.txt_out1.Bind(wx.EVT_TEXT, self.evento_out1_text )
        self.select_device.Bind(wx.EVT_COMBOBOX , self.evento_select_device)
        #### End Eventos botones ######

        self.result_tamanio = ( 580, 200 )
        self.txt_result = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_AUTO_SCROLL, pos=( 30, 300 ),
                                      size=( self.result_tamanio ))
        self.txt_result.SetBackgroundColour( wx.BLACK )
        self.txt_result.SetEditable(False)
        self.txt_result.SetForegroundColour( wx.RED )
        #self.txt_result.setLabel("\n\n\n\nsdasdasdsa")

        self.cb_devices = wx.ComboBox(self.panel, pos=( 131, 522 ), size=( 290, -1 ), style=wx.CB_READONLY)
        #choices
        self.cb_devices.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self._thread = None
        self.item = None
        self.btn_ip.Disable()
        self.btn_puerto.Disable()
        self.btn_desconectar.Disable()
        self.btn_out1.Disable()
        self.btn_out2.Disable()
        self.btn_out3.Disable()
        self.btn_out4.Disable()
        self.btn_out5.Disable()
        self.btn_out6.Disable()
        self.btn_verificar.Disable()
        self.select_device.Disable()


    def serialWatcher(self):
        while True:
            try:
                if self.puerto_serial.inWaiting() and not self.puerto_serial.closed :
                    valor = str(self.puerto_serial.read(self.puerto_serial.inWaiting()).encode('utf-8'))
                    self.txt_result.SetValue( " Mic >> "+valor+"\n"+self.txt_result.GetValue() )
            except:
                continue
            #self.puerto_serial.flushInput()
            time.sleep( .1 )

    def evento_ip(self, evt):
        if self.txt_ip.GetBackgroundColour() == (255, 255, 255, 255):
            trama = chr(2)+chr(108)
            for dato in self.txt_ip.GetValue():
                trama = trama + chr( ord(dato) )
            trama = trama+chr(3)
            self.mensaje_serial( trama )
        else:
            self.txt_result.SetValue(" PC >> Ingrese una ip valida"+"\n"+self.txt_result.GetValue() )

    def evento_puerto(self, evt):
        if self.txt_puerto.GetBackgroundColour() == (255, 255, 255, 255):
            trama = chr(2)+chr(109)
            for dato in self.txt_puerto.GetValue():
                trama = trama + chr( ord(dato) )
            trama = trama+chr(3)
            self.mensaje_serial( trama )
            print trama
        else:
            self.txt_result.SetValue(" PC >> Ingrese un puerto valido"+"\n"+self.txt_result.GetValue() )

    def evento_select_device(self, evt):
        dispositivo = self.lista_devices.keys()[ int(self.select_device.GetSelection()) ]
        if int(self.select_device.GetSelection()) == 0:
            self.btn_ip.Enable()
            self.btn_puerto.Enable()
            self.txt_ip.Enable()
            self.txt_puerto.Enable()
        else:
            trama = chr(2)+chr(103)+str(dispositivo)+chr(3)
            self.mensaje_serial( trama )
            self.txt_ip.Disable()
            self.txt_puerto.Disable()
            self.btn_ip.Disable()
            self.btn_puerto.Disable()
        self.txt_result.SetValue(" PC >> "+str( dispositivo )+" elegido "+"\n"+self.txt_result.GetValue() )

    def evento_out1_text(self, evt):
        hexas = ''
        for digito in self.txt_out1.GetValue():
            hexas = hexas + hex(int(digito)+48)
        self.txt_hex1.SetValue(str(hexas))
        print hexas

    def telf3(self, evt):
        if len(self.txt_telf3.GetValue()) == 8:
            datos = self.mensaje_serial(str(self.txt_telf3.GetValue()) + "*c\n", 2)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("Fallo en telefono 3")

    # funciones de activacion
    def actv1(self, evt):
        if len(self.txt_actv1.GetValue()) > 0:
            datos = self.mensaje_serial(str(self.txt_actv1.GetValue()) + "*e\n", 2.5)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("Fallo en activacion 1")

    def actv2(self, evt):
        if len(self.txt_actv2.GetValue()) > 0:
            datos = self.mensaje_serial(str(self.txt_actv2.GetValue()) + "*f\n", 2.5)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("Fallo en activacion 2")

    def actv3(self, evt):
        if len(self.txt_actv3.GetValue()) > 0:
            datos = self.mensaje_serial(str(self.txt_actv3.GetValue()) + "*g\n", 2.5)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("Fallo en activacion 3")

    #funciones de entrada

    def ent1(self, evt):
        if len(self.txt_disp_ent1.GetValue()) > 0:
            self.txt_result.SetLabel(str(self.txt_disp_ent1.GetValue()) + "*h\n")
            datos = self.mensaje_serial(str(self.txt_disp_ent1.GetValue()) + "*h\n", 3)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("Fallo en entrada 1")

    def ent2(self, evt):
        if len(self.txt_disp_ent2.GetValue()) > 0:
            self.txt_result.SetLabel(str(self.txt_disp_ent2.GetValue()) + "*i\n")
            datos = self.mensaje_serial(str(self.txt_disp_ent2.GetValue()) + "*i\n", 3)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("Fallo en entrada 2")

    def ent3(self, evt):
        if len(self.txt_disp_ent3.GetValue()) > 0:
            self.txt_result.SetLabel(str(self.txt_disp_ent3.GetValue()) + "*j\n")
            datos = self.mensaje_serial(str(self.txt_disp_ent3.GetValue()) + "*j\n", 3)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("Fallo en entrada 3")

    def ent4(self, evt):
        if len(self.txt_disp_ent4.GetValue()) > 0:
            self.txt_result.SetLabel(str(self.txt_disp_ent4.GetValue()) + "*k\n")
            datos = self.mensaje_serial(str(self.txt_disp_ent4.GetValue()) + "*k\n", 3)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("Fallo en telefono 3")

    def numtelf(self, evt):
        datos = self.mensaje_serial("*l\n", 0.5)
        self.txt_result.SetLabel(datos + "\n")

    def tiempo(self, evt):
        if self.txt_tiempo.GetValue().isdigit():
            datos = self.mensaje_serial(hex(int(self.txt_tiempo.GetValue())) + "*d\n", 1.3)
            self.txt_result.SetLabel(datos)
        else:
            self.txt_result.SetLabel("No se pudo establecer el tempo \n ingrese numeros")

    def buscar_seriales(self, evt):
        self.txt_result.SetValue(" PC >> Buscando Dispositivos por puerto serial"+"\n"+self.txt_result.GetValue() )
        self.devs_list = [];
        self.lista_devs = []
        self.txt_result.SetValue(" | ")
        lista_disp = list(list_ports.comports())
        for index in range(len(lista_disp)):
            if lista_disp[index][2] != "n/a" and "Bluetooth" not in lista_disp[index][1]:
                self.devs_list.append(lista_disp[index][0])
                self.lista_devs.append(lista_disp[index][1])
                self.txt_result.SetLabel(self.txt_result.GetLabel() + lista_disp[index][0] + " | ")
                self.txt_result.SetSize( self.result_tamanio )
        print lista_disp
        self.cb_devices.SetItems(self.lista_devs)
        self.cb_devices.SetSelection(0)
        self.cb_devices.SetFocus()


    def OnSelect(self, event):
        self.item = self.cb_devices.GetSelection()
        print self.item

    def conectar_dispositivo(self, evt):
        self.puerto_serial = serial.Serial(str(self.devs_list[self.cb_devices.GetSelection()]), 19200)
        self.txt_result.SetValue(" Conectado a %s" % str(self.devs_list[self.cb_devices.GetSelection()]))
        self.mensaje_serial("*******")
        self.txt_result.SetSize(self.result_tamanio)
        self.item = self.cb_devices.GetSelection()
        self.btn_conectar.Disable()
        self.btn_ip.Enable()
        self.btn_puerto.Enable()
        self.btn_out1.Enable()
        self.btn_out2.Enable()
        self.btn_out3.Enable()
        self.btn_out4.Enable()
        self.btn_out5.Enable()
        self.btn_out6.Enable()
        self.btn_verificar.Enable()
        self.select_device.Enable()
        self.btn_desconectar.Enable()
        self._thread = threading.Thread(target=self.serialWatcher, args=())
        self._thread.setDaemon(True)
        self._thread.start()

    def verificar_dispositivo(self, evt):
        datos = self.mensaje_serial("H\n", 0.3)
        self.txt_result.SetLabel("\n" + datos + "\n")
        self.txt_result.SetSize(self.result_tamanio)

    def desconectar_dispositivo(self, evt):
        self.puerto_serial.close()
        #de : " + str(self.lista_devs[]
        print self.item
        self.txt_result.SetValue(" Desconectado" )
        self.txt_result.SetSize(self.result_tamanio)
        self.btn_conectar.Enable()
        self.btn_ip.Disable()
        self.btn_puerto.Disable()
        self.btn_out1.Disable()
        self.btn_out2.Disable()
        self.btn_out3.Disable()
        self.btn_out4.Disable()
        self.btn_out5.Disable()
        self.btn_out6.Disable()
        self.btn_verificar.Disable()
        self.select_device.Disable()
        self.btn_desconectar.Disable()

    def mensaje_serial(self, mensaje ):
        #self.puerto_serial.flushInput()
        self.puerto_serial.write(mensaje )
        self.txt_result.SetValue( " PC >> "+str( mensaje[1:-1] )+"\n"+self.txt_result.GetValue() )

def main():
    app = wx.App(None)
    frame = Main()
    frame.Show()
    frame.buscar_seriales(None)
    app.MainLoop()


if __name__ == '__main__':
    main()
