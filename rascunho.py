class EffectManager:
    def __init__(self):
        self._active = {}

    def add(self, *effects):  # ('speed', +-0.3, 2)
        active = self._active
        for effect in effects:
            effect_name, rate, turns = effect
            effect_type = 'positive' if rate > 0.0 else 'negative'

            # Usar setdefault para garantir que as chaves existam
            effect_data = active.setdefault(
                effect_name, {}
            ).setdefault(
                effect_type, {'rate': 0.0, 'turn': 0, 'new': True}
            )

            # Atualizar somente se as novas condições forem melhores
            if abs(rate) >= abs(effect_data['rate']) and turns >= effect_data['turn']:
                effect_data.update({'rate': rate, 'turn': turns, 'new': True})

        return active

# Exemplo de uso
manager = EffectManager()
manager.add(('speed', 0.3, 2), ('speed', -0.15, 3))
print(manager._active)