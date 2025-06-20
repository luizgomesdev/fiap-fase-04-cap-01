import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

def create_sample_data():
    """Cria dados sintéticos para treinamento do modelo"""
    np.random.seed(42)
    
    n_samples = 1000
    
    data = {
        'umidade': np.random.uniform(10, 90, n_samples),
        'ph': np.random.uniform(4, 10, n_samples),
        'p': np.random.randint(0, 2, n_samples),
        'k': np.random.randint(0, 2, n_samples)
    }
    

    irrigou = []
    for i in range(n_samples):
        need_water = (data['umidade'][i] < 40.0) and (data['p'][i] == 1 or data['k'][i] == 1)
        irrigou.append(1 if need_water else 0)
    
    data['irrigou'] = irrigou
    
    return pd.DataFrame(data)

def train_model():
    """Treina o modelo de classificação"""
    print("🌱 FarmTech ML - Treinando modelo de irrigação...")
    
    df = create_sample_data()
    
    os.makedirs('src/data', exist_ok=True)
    df.to_csv('src/data/training_data.csv', index=False)
    print(f"📊 Dados de treinamento salvos: {len(df)} amostras")
    
    X = df[['umidade', 'ph', 'p', 'k']]
    y = df['irrigou']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"🎯 Acurácia do modelo: {accuracy:.2%}")
    print("\n📈 Relatório de classificação:")
    print(classification_report(y_test, y_pred))
    
    os.makedirs('src/models', exist_ok=True)
    with open('src/models/irrigation_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("✅ Modelo salvo em 'src/models/irrigation_model.pkl'")
    
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🔍 Importância das features:")
    print(feature_importance)
    
    return model

def predict_irrigation(umidade, ph, p, k):
    """Função para fazer predições com o modelo treinado"""
    try:
        with open('src/models/irrigation_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        input_data = pd.DataFrame({
            'umidade': [umidade],
            'ph': [ph],
            'p': [p],
            'k': [k]
        })
        
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)
        
        return {
            'irrigar': bool(prediction[0]),
            'probabilidade': float(probability[0][1])
        }
    except FileNotFoundError:
        print("❌ Modelo não encontrado. Execute o treinamento primeiro.")
        return None

if __name__ == "__main__":
    model = train_model()
    
    print("\n🧪 Teste de predição:")
    test_cases = [
        (30, 6.5, 1, 0),  # Baixa umidade, deficiência de P
        (60, 7.0, 0, 0),  # Alta umidade, sem deficiências
        (35, 5.5, 0, 1),  # Baixa umidade, deficiência de K
    ]
    
    for umidade, ph, p, k in test_cases:
        result = predict_irrigation(umidade, ph, p, k)
        if result:
            print(f"Umidade: {umidade}%, pH: {ph}, P: {p}, K: {k} → "
                  f"Irrigar: {result['irrigar']} (prob: {result['probabilidade']:.2%})")
