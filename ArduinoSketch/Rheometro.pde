int led0 = 13;
int led1 = 12;
int led2 = 8;
int led3 = 7;
char input = ' ';

void setup() {
  pinMode(led0, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(A0);
  Serial.println(sensorValue, DEC);

  if (Serial.available() > 0){
    input = Serial.read();
  }

  switch (input){
    case 'A':
      digitalWrite(led0, HIGH);
      input = ' ';
      break;
    case 'B':
      digitalWrite(led0, LOW);
      input = ' ';
      break;
    case 'C':
      digitalWrite(led1, HIGH);
      input = ' ';
      break;
    case 'D':
      digitalWrite(led1, LOW);
      input = ' ';
      break;
    case 'E':
      digitalWrite(led2, HIGH);
      input = ' ';
      break;
    case 'F':
      digitalWrite(led2, LOW);
      input = ' ';
      break;
    case 'G':
      digitalWrite(led3, HIGH);
      input = ' ';
      break;
    case 'H':
      digitalWrite(led3, LOW);
      input = ' ';
      break;
  }
}
