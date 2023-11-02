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
    objects = DescriptorBasis(OM.ValidateDict)
    rect = DescriptorBasis(OM.pygame.Rect)
    position = OM.PositionDescriptor(tuple, list, OM.numpy.ndarray)
    size = ObjectSizeDescriptor(tuple, list, OM.numpy.ndarray)

    def __init__(self):
        """ initial itself """
        self.objects = self.ValidateDict(...)
        self.rect = self.pygame.Rect(0, 0, 0, 0)
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
        self.update(owners)

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


class UI(Object):
    """ Object management class """

    def __init__(self):
        """ initial variable """
        super().__init__()
        # super class
        self.__SUPER_CLASS = UI
        return

    @property
    def _SUPER_CLASS(self):
        """ class UI """
        return self.__SUPER_CLASS

    @_abc.abstractmethod
    def update(self, owners: tuple):
        """
            update itself
        :param owners: tuple["owner class", ]
        """
        return


class Application(ObjectManagementBasis):
    """ UI management inheritance class """

    # super class
    OM = ObjectManagementBasis

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

        def __setitem__(self, key, value: UI):
            """ set item """
            if value._SUPER_CLASS not in self.__built_in_types:
                raise TypeError(f"Not match built-in types: {type(value)}")
            super().__setitem__(key, value)
            return

    class __ValidateAssignmentList(list):
        """ event management list object """

        def __setitem__(self, key, value):
            """ set value """
            raise TypeError(f"Not match built-in types: {type(value)}")

    class __ValidateAssignmentInt(int):
        ...

    class __ValidateAssignmentTuple(tuple):
        ...

    class UISuperClassDescriptor(DescriptorBasis):
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
    UIs = DescriptorBasis(SuperClassValidateDict)
    master = OM.SurfaceDescriptor(OM.pygame.Surface)
    rect = DescriptorBasis(OM.pygame.Rect)
    size = OM.SizeDescriptor()

    events = DescriptorBasis(__ValidateAssignmentList)
    key_pressed = DescriptorBasis(OM.pygame.key.ScancodeWrapper)
    key_mods = DescriptorBasis(__ValidateAssignmentInt)
    mouse_pressed = DescriptorBasis(__ValidateAssignmentTuple)
    mouse_pos = DescriptorBasis(__ValidateAssignmentTuple)

    start_UI_key = DescriptorBasis(str, tuple, None)
    execute_UI: UI = UISuperClassDescriptor(UI)

    frame_count = DescriptorBasis(__ValidateAssignmentInt)

    def __init__(self, title: str, icon_surface: OM.pygame.Surface = None):
        """ initial itself """
        # import display config
        from pgapp import display_config
        self.display_config = display_config

        # initial variables
        self.UIs = self.SuperClassValidateDict(UI)
        self.rect = self.OM.pygame.Rect((0, 0, 0, 0))

        # setup display
        self.master = self.pygame.display.set_mode(self.display_config["size"])
        self.pygame.display.set_caption(title)
        if icon_surface is not None:
            self.pygame.display.set_icon(icon_surface)

        # setup UI variables
        self.start_UI_key = None
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
            self.events: Application.__ValidateAssignmentList[Application.pygame.event.Event] = \
                self.__ValidateAssignmentList(self.pygame.event.get())
            self.key_pressed = self.pygame.key.get_pressed()
            self.key_mods = self.__ValidateAssignmentInt(self.pygame.key.get_mods())
            self.mouse_pressed = self.__ValidateAssignmentTuple(self.pygame.mouse.get_pressed())
            self.mouse_pos = self.__ValidateAssignmentTuple(self.pygame.mouse.get_pos())

            # forced termination
            if self.key_pressed[self.pygame.K_DELETE]:
                break

            # event check
            for event in self.events:
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
