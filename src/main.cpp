#include <Arduino.h>
#include "DHT.h"
#include <LiquidCrystal_I2C.h>

// === OTIMIZAÇÕES DE MEMÓRIA ===
// uint8_t: 1 byte ao invés de int (4 bytes) - economia de 75%
// Para pinos GPIO, valores máximo é 48 no ESP32
const uint8_t P_PIN = 12;        // Economiza 3 bytes vs int
const uint8_t K_PIN = 13;        // Economiza 3 bytes vs int
const uint8_t LDR_PIN = 36;      // Economiza 3 bytes vs int
const uint8_t DHT_PIN = 14;      // Economiza 3 bytes vs int
const uint8_t RELAY_PIN = 27;    // Economiza 3 bytes vs int
const uint8_t LED_PIN = 2;       // Economiza 3 bytes vs int

// Constantes para cálculos - armazenadas na Flash, não na RAM
const float HUMIDITY_LIMIT = 40.0;  // Limiar de umidade
const uint16_t ADC_MAX = 4095;      // ADC ESP32 é 12-bit (0-4095)
const uint8_t PH_SCALE = 14;        // pH varia de 0-14

DHT dht(DHT_PIN, DHT22);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  Serial.println("Sistema de Irrigacao Iniciado!");

  pinMode(P_PIN, INPUT);
  pinMode(K_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  dht.begin();
  lcd.init();
  lcd.backlight();
  
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  // === LEITURA DOS SENSORES ===
  // bool: 1 byte - mais eficiente que int para valores 0/1
  bool hasP = digitalRead(P_PIN);
  bool hasK = digitalRead(K_PIN);
  
  // uint16_t: 2 bytes - suficiente para ADC 12-bit (0-4095)
  uint16_t rawLDR = analogRead(LDR_PIN);
  
  // float: necessário para precisão dos sensores DHT
  float humidity = dht.readHumidity();

  // === VALIDAÇÃO E VALORES PADRÃO ===
  if (isnan(humidity)) {
    humidity = 35.0;  // Valor padrão otimizado
  }

  // === CÁLCULOS OTIMIZADOS ===
  // Uso de constantes pré-definidas evita magic numbers
  float pH_value = (rawLDR * (float)PH_SCALE) / (float)ADC_MAX;

  // === LÓGICA DE CONTROLE ===
  // bool: 1 byte - eficiente para flags
  bool needWater = (humidity < HUMIDITY_LIMIT) && (hasP || hasK);
  
  // === CONTROLE DE HARDWARE ===
  digitalWrite(RELAY_PIN, needWater ? HIGH : LOW);
  digitalWrite(LED_PIN, needWater ? HIGH : LOW);

  // === DISPLAY LCD ===
  lcd.setCursor(0, 0);
  lcd.print("U:");
  lcd.print(humidity, 1);
  lcd.print("% pH:");
  lcd.print(pH_value, 1);
  
  lcd.setCursor(0, 1);
  lcd.print("P:");
  lcd.print(hasP);
  lcd.print(" K:");
  lcd.print(hasK);
  lcd.print(" Pump:");
  lcd.print(needWater ? 1 : 0);

  // === SERIAL PLOTTER - MÚLTIPLAS VARIÁVEIS ===
  // Formato: Humidity:valor pH:valor Pump:valor
  // Permite monitorar 3 variáveis simultaneamente
  Serial.print("Humidity:");
  Serial.print(humidity);
  Serial.print(" pH:");
  Serial.print(pH_value);
  Serial.print(" Pump:");
  Serial.println(needWater ? 100 : 0);  // Pump como 0/100 para visualização

  delay(1000);  // 1 segundo - otimizado para responsividade
}