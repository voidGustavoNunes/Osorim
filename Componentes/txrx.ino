// Programa: Comunicacao Serial Arduino com Raspberry Pi
// Autor: Henrique Almeida

char buf;
int incomingByte;
 
void setup(){
  Serial.begin(9600);
  /* initialize random seed: */
  randomSeed(analogRead(0));

}
 
void loop(){
  //delay(2000);
  
  if (Serial.available() > 0) {
    // lê o dado recebido:
    incomingByte = Serial.read();
    buf = random(97,123);
    // Caso seja recebido o caracter significativo
    if (incomingByte!='\n'){
      // Envia a resposta para o Raspberry
      delay(200);
      Serial.print((char)incomingByte);
      Serial.print(" recebido! - Bit: ");
      Serial.println(buf);
    }
  }
}
