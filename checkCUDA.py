import torch

# Проверяем доступность CUDA
if torch.cuda.is_available():
    # Создаем устройство CUDA
    device = torch.device("cuda")
    print("CUDA доступен")
else:
    # Если CUDA недоступен, используем CPU
    device = torch.device("cpu")
    print("CUDA недоступен, используем CPU")

# Пример создания тензора и перемещения его на устройство CUDA
x = torch.tensor([1, 2, 3]).to(device)