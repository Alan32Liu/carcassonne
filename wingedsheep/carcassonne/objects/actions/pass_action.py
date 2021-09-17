from wingedsheep.carcassonne.objects.actions.action import Action


class PassAction(Action):
    pass

    def __eq__(self, other: 'PassAction'):
        return isinstance(other, PassAction)
