# import abc
import abc as _abc
# import format
from pgapp._format import DescriptorBasis


class ObjectManagementBasis(_abc.ABC):
    """ Surface management inheritance class basis """
    # import pygame and numpy
    import pygame
    import numpy

    class ValidateDict(dict):
        """ object manage dict object """

        def __init__(self, *built_in_types: object):
            """ initial itself """
            self.__built_in_types = built_in_types
            super().__init__()
            return

        @property
        def built_in_types(self):
            """ registered built_in_types """
            return self.__built_in_types

        def __setitem__(self, key, value):
            """ set item """
            if type(value) not in self.__built_in_types:
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
            instance.__dict__["rect"][2:] = instance.__dict__[self.name].get_rect()[2:]
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

    class SuperClassValidateDict(dict):
        """ super class validate dict class """

        def __init__(self, *built_in_types: object):
            """ initial itself """
            self.__built_in_types = built_in_types
            super().__init__()
            return

        @property
        def built_in_types(self):
            """ registered built_in_types """
            return self.__built_in_types

        def __setitem__(self, key, value):
            """ set item """
            if value._SUPER_CLASS not in self.__built_in_types:
                raise TypeError(f"Not match built-in types: {type(value._SUPER_CLASS)} : built-in types{self.__built_in_types}")
            super().__setitem__(key, value)
            return


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
    objects = DescriptorBasis(OM.SuperClassValidateDict)
    rect = DescriptorBasis(OM.pygame.Rect)
    position = OM.PositionDescriptor(tuple, list, OM.numpy.ndarray)
    size = ObjectSizeDescriptor(tuple, list, OM.numpy.ndarray)
    killing = DescriptorBasis(bool)

    def __init__(self):
        """ initial itself """
        # super class
        self._SUPER_CLASS = Object
        # itself
        self.objects: dict = self.SuperClassValidateDict(Object, Surface)
        self.rect = self.pygame.Rect(0, 0, 0, 0)
        self.killing = False
        return

    @_abc.abstractmethod
    def update(self, owners: tuple):
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
        self.update(owners)

        # objects
        for object_ in self.objects.values():
            object_._execute_update((*owners, self))
            continue

        # kill object
        objects_dum = self.OM.SuperClassValidateDict(Object, Surface)
        for key, object_ in self.objects.items():
            if object_.killing:
                continue
            objects_dum[key] = object_
            continue
        self.objects = objects_dum

        return

    def _execute_draw(self, *args):
        """ execute draw functions """
        # objects
        for object_ in self.objects.values():
            object_._execute_draw(*args)
            continue
        return

    def copy(self):
        """ copy itself """
        return self.__copy()

    def kill(self):
        """ kill self """
        self.killing = True
        return


class Surface(Object):
    """ Surface management class """
    # constance variables
    OB = Object

    class SurfaceSizeDescriptor(OB.ObjectSizeDescriptor):
        """ descriptor for size of object variable """
        OB = Object

        def __set__(self, instance, value):
            """ set value """
            super().__set__(instance, value)
            instance.__dict__["surface"] = self.OB.pygame.Surface(value)
            return

    # instance
    surface = DescriptorBasis(OB.pygame.Surface)
    size = SurfaceSizeDescriptor(tuple, list, OB.numpy.ndarray)
    objects: dict

    def __init__(self, size: tuple[int, int]):
        """ initial surface and variables """
        super().__init__()
        # super class
        self._SUPER_CLASS = Surface
        # surface
        self.surface = self.OB.pygame.Surface(size)
        return

    @_abc.abstractmethod
    def update(self, owners: tuple):
        """
            update itself
        :param owners: tuple["owner class", ]
        """
        return

    def draw(self, master: OB.pygame.Surface):
        """
            draw itself
        :param master: display surface object
        """
        master.blit(self.surface, self.rect)
        return

    def _execute_draw(self, *args):
        """ execute draw function """
        self.draw(*args)
        super()._execute_draw(*args)
        return


class UI(Object):
    """ Object management class """
    # constance variables
    OB = Object
    # instance variables
    background = DescriptorBasis(tuple, str)
    objects: dict

    def __init__(self, background_color: str | tuple[int, int, int] = "black"):
        """ initial variable """
        super().__init__()
        # super class
        self._SUPER_CLASS = UI
        # instance variables
        self.background: str | tuple[int, int, int] = background_color
        return

    @_abc.abstractmethod
    def update(self, owners: tuple):
        """
            update itself
        :param owners: tuple["owner class", ]
        """
        return

    def _execute_draw(self, master, *args):
        """ execute draw functions """
        master.fill(self.background)
        super()._execute_draw(master, *args)
        return


class Application(ObjectManagementBasis):
    """ UI management inheritance class """

    # super class
    OM = ObjectManagementBasis

    class __ValidateAssignmentList(list):
        """ event management list object """

        def __setitem__(self, key, value):
            """ set value """
            raise TypeError(f"Not match built-in types: {type(value)}")

    class __ValidateAssignmentInt(int):
        ...

    class __ValidateAssignmentTuple(tuple):
        ...

    class __UISuperClassDescriptor(DescriptorBasis):
        """ descriptor for UI """

        def __set__(self, instance: object, value: UI):
            """ set value """
            # validate built-in type
            if (value._SUPER_CLASS not in self.built_in_types) and not (value is None and None in self.built_in_types):
                raise TypeError(f"Not match built-in types: {type(value)}")

            # validate function
            self.validate(value)

            # set value
            instance.__dict__[self.name] = value
            return

    # instance variables
    UIs = DescriptorBasis(OM.SuperClassValidateDict)
    master = OM.SurfaceDescriptor(OM.pygame.Surface)
    rect = DescriptorBasis(OM.pygame.Rect)
    size = OM.SizeDescriptor()

    get_events = DescriptorBasis(__ValidateAssignmentList)
    get_key_pressed = DescriptorBasis(OM.pygame.key.ScancodeWrapper)
    get_key_mods = DescriptorBasis(__ValidateAssignmentInt)
    get_mouse_pressed = DescriptorBasis(__ValidateAssignmentTuple)
    get_mouse_pos = DescriptorBasis(__ValidateAssignmentTuple)

    start_UI_key = DescriptorBasis(str, tuple, None)
    execute_UI: UI = __UISuperClassDescriptor(UI)

    frame_count = DescriptorBasis(__ValidateAssignmentInt)

    def __init__(self,
                 title: str,
                 icon_surface: OM.pygame.Surface = None,
                 UIs: dict = None,
                 start_UI_key: str = None
                 ):
        """ initial itself """
        # import display config
        from pgapp import display_config
        self.display_config = display_config

        # initial variables
        self.UIs = self.SuperClassValidateDict(UI)
        if UIs is not None:
            for key, value in UIs.items():
                self.UIs[key] = value
        self.rect = self.OM.pygame.Rect((0, 0, 0, 0))

        # setup display
        self.master = self.pygame.display.set_mode(self.display_config["size"])
        self.pygame.display.set_caption(title)
        if icon_surface is not None:
            self.pygame.display.set_icon(icon_surface)

        # setup UI variables
        self.start_UI_key = start_UI_key
        return

    def changing_UI(self, UI_key: str | tuple):
        """
            changing Ui function
        :param UI_key: registered key of UI that you want to change
        """
        self.execute_UI = self.UIs[UI_key].copy()
        return

    def exe(self):
        """ execute me """
        # pygame setup
        self.pygame.init()

        # UI setup
        if self.start_UI_key is None:
            raise TypeError(f"The start UI key is not registered: start_UI_Kay")
        self.changing_UI(self.start_UI_key)

        # setup frame
        self.frame_count = self.__ValidateAssignmentInt(0)
        clock = self.pygame.time.Clock()

        # mainloop
        done = False
        while not done:
            # count up
            self.frame_count = self.__ValidateAssignmentInt(self.frame_count + 1)

            # get input data of pygame
            self.get_events: Application.__ValidateAssignmentList[Application.pygame.event.Event] = \
                self.__ValidateAssignmentList(self.pygame.event.get())
            self.get_key_pressed = self.pygame.key.get_pressed()
            self.get_key_mods = self.__ValidateAssignmentInt(self.pygame.key.get_mods())
            self.get_mouse_pressed = self.__ValidateAssignmentTuple(self.pygame.mouse.get_pressed())
            self.get_mouse_pos = self.__ValidateAssignmentTuple(self.pygame.mouse.get_pos())

            # forced termination
            if self.get_key_pressed[self.pygame.K_DELETE]:
                break

            # event check
            for event in self.get_events:
                # QUIT
                if event.type == self.pygame.QUIT:
                    done = True

            # update
            self.execute_UI._execute_update((self, ))

            # draw
            self.execute_UI._execute_draw(self.master)
            self.pygame.display.update()

            # frame rate
            clock.tick(self.display_config["framerate"])
            continue

        return
