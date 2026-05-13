import constantes as C


offset = C.HITBOX_OFFSET
size = C.HITBOX_SIZE

offset = C.mundo_p_tela(offset[0], offset[1])
size = C.mundo_p_tela(size[0], size[1])

print(offset)
print(size)