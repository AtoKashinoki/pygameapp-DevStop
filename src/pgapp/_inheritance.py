# import abc
import abc as _abc
# import format
from pgapp._format import DescriptorBasis


class ObjectManagementBasis(_abc.ABC):
    """ Surface management inheritance class basis """
    # import pygame and numpy
    import pygame
    import numpy

    class ObjectDict(dict):
        """ object manage dict object """

        def __setitem__(self, key, value):
            """ set item """
            if type(value) not in (str, ):
                raise TypeError(f"Not match built-in types: {type(value)}")
            super().__setitem__(key, value)
            return

    class SurfaceDescriptor(DescriptorBasis):
        """ descriptor for surface variable """

        def __set__(self, instance: object, value):
            """ set value """
            super().__set__(instance, value)
            if value is None:
                return
            instance.__dict__["rect"][2:] = instance.__dict__["surface"].get_rect()[2:]
            return

    class CoordinateDescriptor(DescriptorBasis):
        """ descriptor for coordinate calculation """
        # import numpy
        import numpy

    class PositionDescriptor(CoordinateDescriptor):
        """ descriptor for position variable """

        def __set__(self, instance: object, value):
            """ set position in rect """
            instance.__dict__["rect"][:2] = value
            return

        def __get__(self, instance: object, owner):
            """ get position in rect """
            return self.numpy.array(instance.__dict__["rect"][:2])

    class SizeDescriptor(CoordinateDescriptor):
        """ descriptor for size variables """

        def __set__(self, instance: object, value):
            raise TypeError(f"It is a read-only variable: {self.name}")

        def __get__(self, instance: object, owner):
            """ get size in rect """
            return self.numpy.array(instance.__dict__["rect"][2:])


class Object(ObjectManagementBasis):
    """ Objects management inheritance class """
    # import copy
    from copy import copy as __copy

    # super class
    OM = ObjectManagementBasis

    class ObjectSizeDescriptor(OM.SizeDescriptor):
        """ descriptor for size of object variable """

        def __set__(self, instance, value):
            """ set value """
            instance.__dict__["rect"][2:] = value
            return

    # instance variables
    objects = DescriptorBasis(OM.ObjectDict)
    rect = DescriptorBasis(OM.pygame.Rect)
    position = OM.PositionDescriptor(tuple, list, OM.numpy.ndarray)
    size = ObjectSizeDescriptor(tuple, list, OM.numpy.ndarray)

    def __init__(self):
        """ initial itself """
        self.objects = self.ObjectDict()
        self.rect = self.pygame.Rect(0, 0, 0, 0)
        self.position = (0, 0)
        return

    @_abc.abstractmethod
    def update(self, *owners: tuple):
        """
            update itself
        :param owners: tuple["owner class", ]
        """
        return

    def _execute_update(self, owners: tuple):
        """
            execute update functions
        :param owners: tuple["owner class", ]
        """
        # itself
        self.update(*owners)

        # objects
        for object_ in self.objects:
            object_._execute_update((*owners, self))
            continue

        return

    def _execute_draw(self, master: OM.pygame.Surface):
        """ execute draw functions """
        # objects
        for object_ in self.objects:
            object_._execute_draw(master)
            continue
        return

    def copy(self):
        """ copy itself """
        return self.__copy()
