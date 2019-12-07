import torch

# x = torch.tensor([5.5, 3])
# print(x)
#
# x = x.new_zeros(5, 3, dtype=torch.double)
# print(x)
#
# x = torch.rand_like(x, dtype=torch.float)
# print(x)
#
# y = torch.rand_like(x, dtype=torch.float)
# print("y=" + str(y))
# print("x=" + str(x))
#
# print("x + y =\n" + str(x+y))

if torch.cuda.is_available():
    print("cuda is available")
    device = torch.device("cuda")          # a CUDA device object
    y = torch.ones_like(x, device=device)  # directly create a tensor on GPU
    x = x.to(device)                       # or just use strings ``.to("cuda")``
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))

