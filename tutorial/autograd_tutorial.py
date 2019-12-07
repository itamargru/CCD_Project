import torch

x = torch.ones(2, 2, requires_grad=True)
print(x)

y = x + 2
print(y)
print(y.grad_fn)

z = y*y*3;
out = z.mean()
print(z, out)

out.backward()
print(x.grad)

x = torch.randn(3, requires_grad=True)
z=torch.ones(3, requires_grad=True)

y = z * x * 2
z.requires_grad_(True)
while y.data.norm() < 1000:
    y = y * 2
    print("==>y=", y)


v = torch.tensor([0.1, 1.0, 0.0001], dtype=torch.float)
u = 2*y
u.backward(v)

print("grad x= ", x.grad)
print("grad z=", z.grad)


print(x.requires_grad)
print((x ** 2).requires_grad)

with torch.no_grad():
    print((x ** 2).requires_grad)