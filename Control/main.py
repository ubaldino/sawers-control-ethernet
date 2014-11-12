#!/usr/bin/python2

#encoding:utf-8
__author__ = 'ubaldino'
__copyright__ = "...."

from optparse import OptionParser
from serial.tools import list_ports
import wx , os , time , serial


class Validate_Numeric( wx.PyValidator ):
	def __init__( Self ):
		wx.PyValidator.__init__( Self )
		Self.Bind( wx.EVT_TEXT , Self.On_Text_Change )
	
	def Clone( Self ):
		return Validate_Numeric()

	def On_Text_Change( Self , Event ):
		TextCtrl = Self.GetWindow()
		Text = TextCtrl.GetValue()
		if Text.isdigit() or Text == "":
			TextCtrl.SetBackgroundColour( "White" )
		else :
			TextCtrl.SetBackgroundColour( "Red" )
		Event.Skip()

class Validate_Numeric_Dot( wx.PyValidator ):
	def __init__( Self ):
		wx.PyValidator.__init__( Self )
		Self.Bind( wx.EVT_TEXT , Self.On_Text_Change )
	
	def Clone( Self ):
		return Validate_Numeric()

	def On_Text_Change( Self , Event ):
		TextCtrl = Self.GetWindow()
		Text = TextCtrl.GetValue()
		if Text.isdigit() or Text == "":
			TextCtrl.SetBackgroundColour( "White" )
		else :
			TextCtrl.SetBackgroundColour( "Red" )
		Event.Skip()

class Validate_Text( wx.PyValidator ):
	def __init__( Self ):
		wx.PyValidator.__init__( Self )
		Self.Bind( wx.EVT_TEXT , Self.On_Text_Change )
	
	def Clone( Self ):
		return Validate_Text()

	def On_Text_Change( Self , Event ):
		TextCtrl = Self.GetWindow()
		Text = TextCtrl.GetValue()
		if not Text.isdigit() or Text == "":
			TextCtrl.SetBackgroundColour( "White" )
		else :
			TextCtrl.SetBackgroundColour( "Pink" )
		Event.Skip()

class Main( wx.Frame ):
	def __init__(self):
		wx.Frame.__init__( self, None, -1, 'Sawers 1.0', size=( 850 , 600 ) )
		self.icon = wx.Icon( os.path.join( os.getcwd() , "resources", "sawers.ico" ) , wx.BITMAP_TYPE_ICO )

		self.SetIcon( self.icon )
		self.panel = wx.Panel( self , -1 )
		self.count_conect = 0
		self.puerto_serial = None


		btn_buscar = wx.Button( self.panel , label='Buscar', pos=( 40 , 520 ))
		btn_conectar = wx.Button( self.panel , label='Conectar', pos=( 430 , 520 ))
		btn_desconectar = wx.Button( self.panel , label='Desconectar', pos=( 510 , 520 ) )
		btn_verificar = wx.Button( self.panel , label='Verificar', pos=( 640 , 520 ) )


        #### Text fomularios ######
		## cambiar de ip
		self.lbl_ip = wx.StaticText( self.panel , label="IP", pos=( 80 , 40 ) )
		self.txt_ip = wx.TextCtrl( self.panel , value="ip" , style=wx.TE_CENTRE , pos=( 40 , 60 ) ,  validator=Validate_Numeric() )
	
		btn_buscar.Bind( wx.EVT_BUTTON , self.buscar_seriales )
		btn_conectar.Bind( wx.EVT_BUTTON , self.conectar_dispositivo )
		btn_desconectar.Bind( wx.EVT_BUTTON , self.desconectar_dispositivo )
		btn_verificar.Bind( wx.EVT_BUTTON , self.verificar_dispositivo )

		self.txt_result = wx.TextCtrl( self.panel , style=wx.TE_MULTILINE | wx.TE_AUTO_SCROLL , pos = ( 40 , 300 ) , size=( 760 , 160 ) )
		self.txt_result.SetBackgroundColour( wx.BLACK )
		self.txt_result.SetEditable(False)
		self.txt_result.SetForegroundColour( wx.RED )

		self.cb_devices = wx.ComboBox( self.panel , pos=( 140, 520 ), size=( 280, -1) , style=wx.CB_READONLY )
		#choices
		self.cb_devices.Bind( wx.EVT_COMBOBOX , self.OnSelect )


	def telf1( self , evt):
		if len( self.txt_telf1.GetValue() ) == 8:
			datos = self.mensaje_serial( str( self.txt_telf1.GetValue() ) + "*a\n" , 2 )
			self.txt_result.SetLabel( datos )
		else:

			self.txt_result.SetLabel( "Fallo en telefono 1" )
	
	def telf2( self , evt):
		if len( self.txt_telf2.GetValue() ) == 8:
			datos = self.mensaje_serial( str( self.txt_telf2.GetValue() ) + "*b\n" , 2 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en telefono 2" )

	def telf3( self , evt):
		if len( self.txt_telf3.GetValue() ) == 8:
			datos = self.mensaje_serial( str( self.txt_telf3.GetValue() ) + "*c\n" , 2 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en telefono 3" )
	# funciones de activacion
	def actv1( self , evt):
		if len( self.txt_actv1.GetValue() ) > 0:
			datos = self.mensaje_serial( str( self.txt_actv1.GetValue() ) + "*e\n" , 2.5 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en activacion 1" )

	def actv2( self , evt):
		if len( self.txt_actv2.GetValue() ) > 0:
			datos = self.mensaje_serial( str( self.txt_actv2.GetValue() ) + "*f\n" , 2.5 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en activacion 2" )

	def actv3( self , evt):
		if len( self.txt_actv3.GetValue() ) > 0:
			datos = self.mensaje_serial( str( self.txt_actv3.GetValue() ) + "*g\n" , 2.5 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en activacion 3" )
	#funciones de entrada
				
	def ent1( self , evt ):
		if len( self.txt_disp_ent1.GetValue() ) > 0:
			self.txt_result.SetLabel( str( self.txt_disp_ent1.GetValue() ) + "*h\n" )
			datos = self.mensaje_serial( str( self.txt_disp_ent1.GetValue() ) + "*h\n" , 3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en entrada 1" )

	def ent2( self , evt ):
		if len( self.txt_disp_ent2.GetValue() ) > 0:
			self.txt_result.SetLabel( str( self.txt_disp_ent2.GetValue() ) + "*i\n" )
			datos = self.mensaje_serial( str( self.txt_disp_ent2.GetValue() ) + "*i\n" , 3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en entrada 2" )

	def ent3( self , evt):
		if len( self.txt_disp_ent3.GetValue() ) > 0:
			self.txt_result.SetLabel( str( self.txt_disp_ent3.GetValue() ) + "*j\n" )
			datos = self.mensaje_serial( str( self.txt_disp_ent3.GetValue() ) + "*j\n" , 3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en entrada 3" )
	
	def ent4( self , evt):
		if len( self.txt_disp_ent4.GetValue() ) > 0:
			self.txt_result.SetLabel( str( self.txt_disp_ent4.GetValue() ) + "*k\n" )
			datos = self.mensaje_serial( str( self.txt_disp_ent4.GetValue() ) + "*k\n" , 3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en telefono 3" )
	
	def numtelf( self , evt ):
		datos = self.mensaje_serial( "*l\n" , 0.5 )
		self.txt_result.SetLabel( datos + "\n" )
	
	def tiempo( self , evt ):
		if self.txt_tiempo.GetValue().isdigit():
			datos = self.mensaje_serial( hex( int( self.txt_tiempo.GetValue() ) )  + "*d\n" , 1.3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "No se pudo establecer el tempo \n ingrese numeros" )

	def buscar_seriales(self , evt ):
		self.devs_list = [] ; self.lista_devs = []
		self.txt_result.SetLabel( " | " )
		lista_disp = list( list_ports.comports() )
		for index in range( len( lista_disp ) ):
			self.devs_list.append( lista_disp[index][0] )
			self.lista_devs.append( lista_disp[index][1] )
			self.txt_result.SetLabel( self.txt_result.GetLabel() + lista_disp[index][0] + " | " )
			self.txt_result.SetSize( ( 760 , 160 ) )
		self.cb_devices.SetItems( self.lista_devs )
		self.cb_devices.SetSelection(0)
		self.cb_devices.SetFocus()


	def OnSelect( self, event ):
		self.item = self.cb_devices.GetSelection()
		print self.item

	def conectar_dispositivo( self , evt ):
		self.puerto_serial = serial.Serial( str( self.devs_list[ self.cb_devices.GetSelection() ] ) , 9600 )
		self.txt_result.SetLabel( "conectado a %s"%str( self.devs_list[ self.cb_devices.GetSelection() ] ) )
		self.txt_result.SetSize( ( 760 , 160 ) )

	def verificar_dispositivo( self , evt ):
		datos = self.mensaje_serial( "H\n" , 0.3 )
		self.txt_result.SetLabel( "\n"+datos + "\n"  )
		self.txt_result.SetSize( ( 760 , 160 ) )

	def desconectar_dispositivo( self , evt ):
		self.puerto_serial.close()
		self.txt_result.SetLabel( "Desconectado de : "+str( self.lista_devs[self.item] ) )
		self.txt_result.SetSize( ( 760 , 160 ) )

	def mensaje_serial( self , mensaje , delay ):
		#self.puerto_serial.flushInput()
		self.puerto_serial.write( mensaje )
		time.sleep( delay )
		return self.puerto_serial.read( self.puerto_serial.inWaiting() )

def main():
    app = wx.App(None)
    frame = Main()
    frame.Show()
    frame.buscar_seriales(None)
    app.MainLoop()

if __name__ == '__main__':
	main()
