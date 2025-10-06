# 📝 Guia de Configuração - Canine AI

Este documento explica detalhadamente como ajustar as configurações do modelo através do arquivo `config.yaml`.

## 📋 Índice

1. [Parâmetros de Detecção](#parâmetros-de-detecção)
2. [Visualização](#visualização)
3. [Filtros de Classes](#filtros-de-classes)
4. [Performance](#performance)
5. [Interface](#interface)
6. [Segurança](#segurança)
7. [Debug e Logging](#debug-e-logging)
8. [Cache](#cache)
9. [Exemplos de Uso](#exemplos-de-uso)

---

## Parâmetros de Detecção

### `confidence_threshold` (padrão: 0.25)
- **Tipo:** Float (0.0 - 1.0)
- **Descrição:** Confiança mínima para uma detecção ser considerada válida
- **Valores maiores:** Menos detecções, mas mais precisas
- **Valores menores:** Mais detecções, mas pode incluir falsos positivos
- **Recomendado:** 0.25 - 0.35 para uso geral

```yaml
confidence_threshold: 0.30  # 30% de confiança mínima
```

### `iou_threshold` (padrão: 0.45)
- **Tipo:** Float (0.0 - 1.0)
- **Descrição:** Threshold de IoU para Non-Maximum Suppression (NMS)
- **Valores maiores:** Permite mais boxes sobrepostos
- **Valores menores:** Suprime mais boxes sobrepostos
- **Recomendado:** 0.40 - 0.50

```yaml
iou_threshold: 0.45
```

### `max_detections` (padrão: 10)
- **Tipo:** Integer
- **Descrição:** Número máximo de detecções por imagem
- **Uso:** Limita o número de cães detectados em uma única imagem

```yaml
max_detections: 10
```

### `image_size` (padrão: 640)
- **Tipo:** Integer
- **Descrição:** Tamanho da imagem para inferência (pixels)
- **Valores comuns:** 320, 416, 640, 1280
- **Maior:** Mais preciso, mas mais lento
- **Menor:** Mais rápido, mas menos preciso

```yaml
image_size: 640  # Equilibrado
# image_size: 1280  # Alta precisão (mais lento)
# image_size: 416   # Rápido (menos preciso)
```

---

## Visualização

### `line_thickness` (padrão: 2)
- **Tipo:** Integer
- **Descrição:** Espessura das linhas das bounding boxes

```yaml
line_thickness: 3  # Linhas mais grossas
```

### `show_labels` (padrão: true)
- **Tipo:** Boolean
- **Descrição:** Mostrar labels das classes nas detecções

```yaml
show_labels: true
```

### `show_confidence` (padrão: true)
- **Tipo:** Boolean
- **Descrição:** Mostrar confiança nos labels

```yaml
show_confidence: true
```

### `confidence_format` (padrão: "percentage")
- **Tipo:** String
- **Opções:** "percentage" ou "decimal"
- **Descrição:** Formato de exibição da confiança

```yaml
confidence_format: "percentage"  # Exibe: 85%
# confidence_format: "decimal"    # Exibe: 0.85
```

---

## Filtros de Classes

### `enable_class_filter` (padrão: false)
- **Tipo:** Boolean
- **Descrição:** Habilitar filtro de classes específicas

### `allowed_classes` (padrão: [])
- **Tipo:** List[Integer]
- **Descrição:** Lista de IDs de classes para detectar (vazio = todas)

```yaml
enable_class_filter: true
allowed_classes: [0, 5, 10, 15]  # Detectar apenas raças específicas
```

### `class_specific_confidence` (padrão: {})
- **Tipo:** Dictionary
- **Descrição:** Confiança mínima por classe

```yaml
class_specific_confidence:
  0: 0.3   # Raça ID 0 precisa apenas 30%
  15: 0.5  # Raça ID 15 precisa 50%
```

---

## Performance

### `use_half_precision` (padrão: false)
- **Tipo:** Boolean
- **Descrição:** Usar half precision (FP16) - mais rápido em GPUs compatíveis
- **Requer:** GPU com suporte a FP16

```yaml
use_half_precision: true  # Habilitar em GPU compatível
```

### `device` (padrão: "cpu")
- **Tipo:** String
- **Opções:** "cpu", "cuda", "cuda:0", "cuda:1", etc.
- **Descrição:** Device para inferência

```yaml
device: "cuda"     # Usar GPU principal
# device: "cuda:0" # Usar GPU 0
# device: "cpu"    # Usar CPU
```

### `use_tensorrt` (padrão: false)
- **Tipo:** Boolean
- **Descrição:** Usar TensorRT para otimização (requer instalação separada)

```yaml
use_tensorrt: false
```

---

## Interface

### `test_images_columns` (padrão: 4)
- **Tipo:** Integer
- **Descrição:** Número de colunas para exibir imagens de teste

```yaml
test_images_columns: 4
```

### `max_upload_size_mb` (padrão: 10)
- **Tipo:** Integer
- **Descrição:** Tamanho máximo de upload (MB)

```yaml
max_upload_size_mb: 20  # Permitir uploads até 20MB
```

### `allowed_formats` (padrão: ["png", "jpg", "jpeg", "webp"])
- **Tipo:** List[String]
- **Descrição:** Formatos de imagem permitidos

```yaml
allowed_formats: ["png", "jpg", "jpeg", "webp", "bmp"]
```

---

## Segurança

### `check_image_dimensions` (padrão: true)
- **Tipo:** Boolean
- **Descrição:** Verificar dimensões da imagem antes de processar

### `max_image_dimension` (padrão: 4096)
- **Tipo:** Integer
- **Descrição:** Dimensão máxima permitida (largura ou altura em pixels)

### `min_image_dimension` (padrão: 32)
- **Tipo:** Integer
- **Descrição:** Dimensão mínima permitida (largura ou altura em pixels)

```yaml
check_image_dimensions: true
max_image_dimension: 4096
min_image_dimension: 32
```

---

## Debug e Logging

### `show_inference_time` (padrão: true)
- **Tipo:** Boolean
- **Descrição:** Exibir tempo de inferência

```yaml
show_inference_time: true
```

### `save_predictions` (padrão: false)
- **Tipo:** Boolean
- **Descrição:** Salvar imagens processadas

### `predictions_dir` (padrão: "predictions")
- **Tipo:** String
- **Descrição:** Diretório para salvar predições

### `verbose` (padrão: false)
- **Tipo:** Boolean
- **Descrição:** Modo verbose (mais informações no console)

```yaml
save_predictions: true
predictions_dir: "outputs"
verbose: true
```

---

## Cache

### `enable_model_cache` (padrão: true)
- **Tipo:** Boolean
- **Descrição:** Habilitar cache do modelo

### `enable_data_cache` (padrão: true)
- **Tipo:** Boolean
- **Descrição:** Habilitar cache de dados

### `cache_ttl` (padrão: 3600)
- **Tipo:** Integer
- **Descrição:** TTL do cache em segundos (0 = infinito)

```yaml
enable_model_cache: true
enable_data_cache: true
cache_ttl: 3600  # 1 hora
```

---

## Exemplos de Uso

### Configuração para Alta Precisão
```yaml
detection:
  confidence_threshold: 0.35
  iou_threshold: 0.50
  image_size: 1280
  max_detections: 15

performance:
  device: "cuda"
  use_half_precision: true
```

### Configuração para Velocidade
```yaml
detection:
  confidence_threshold: 0.25
  iou_threshold: 0.40
  image_size: 416
  max_detections: 5

performance:
  device: "cuda"
  use_half_precision: true
```

### Configuração para Produção
```yaml
detection:
  confidence_threshold: 0.30
  iou_threshold: 0.45
  image_size: 640
  max_detections: 10

debug:
  show_inference_time: true
  save_predictions: true
  predictions_dir: "production_outputs"

security:
  check_image_dimensions: true
  max_image_dimension: 4096
  min_image_dimension: 100
```

### Configuração para CPU (sem GPU)
```yaml
detection:
  confidence_threshold: 0.25
  iou_threshold: 0.45
  image_size: 640
  max_detections: 10

performance:
  device: "cpu"
  use_half_precision: false

cache:
  enable_model_cache: true
  enable_data_cache: true
  cache_ttl: 7200
```

---

## 🔄 Aplicando Mudanças

1. **Edite o arquivo `config.yaml`** com suas configurações
2. **Salve o arquivo**
3. **Recarregue a aplicação:**
   - Use o botão "🔄 Recarregar Config" na sidebar, OU
   - Faça uma nova predição (mudanças são aplicadas automaticamente)
4. **Verifique as configurações ativas** na sidebar do app

---

## ⚠️ Avisos Importantes

- Valores muito baixos de `confidence_threshold` podem gerar muitos falsos positivos
- `image_size` maior consome mais memória
- `use_half_precision` requer GPU com suporte a FP16
- Sempre teste as configurações antes de usar em produção
- Mantenha backup do `config.yaml` original

---

## 🆘 Solução de Problemas

**Erro: "Modelo muito lento"**
- Reduza `image_size` para 416 ou 320
- Habilite `use_half_precision` se tiver GPU
- Reduza `max_detections`

**Erro: "Muitos falsos positivos"**
- Aumente `confidence_threshold` para 0.30 - 0.40
- Ajuste `iou_threshold` para 0.50

**Erro: "Não detecta nada"**
- Reduza `confidence_threshold` para 0.20 - 0.25
- Verifique se a imagem contém cães
- Aumente `image_size` para 1280

**Erro: "Memória insuficiente"**
- Reduza `image_size`
- Desabilite `use_half_precision`
- Use `device: "cpu"`

---

**🐕 Canine AI** - Sistema Inteligente de Reconhecimento de Raças Caninas

