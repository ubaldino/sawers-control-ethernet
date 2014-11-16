
byte valores[18];
String retorno = "";

void lector(){
	bool band = false; retorno = "";

	while( Serial.available() ){
		
		byte valor = Serial.read();
		
		if( 2 == valor ){ band = true; }
		
		if( 3 == valor ){
			band = false;
			while( Serial.available() ){ Serial.read(); }
		}
		
		if( band == true && 2 != valor ){
			retorno += (char) valor;
		}
		delay(4);
	}
}

void setup() {
	Serial.begin(19200);
}

void loop() {
	if( Serial.available() ){
		lector();
		Serial.print( retorno );
	}
	delay(5);
}
