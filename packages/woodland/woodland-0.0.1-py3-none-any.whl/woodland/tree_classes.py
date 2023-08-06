"""This file contains the classes for creating Trees.

This file contains the classes for creating Trees along with their functions
for retrieving attributes and generating instances.
"""
from typing import Any


class TreeNode:
    """Use this class to create a Node for the tree structure.

    This class is used for creating a 'TreeNode' Node instance for populating the
    tree data structure with.
    """

    def __init__(
        self,
        node_id: int = None,
        payload: Any = None,
        children: list = None,
        parent: "TreeNode" = None,
    ) -> None:
        """Use this function to initialise an instance of the TreeNode class.

        This function is used for initialising an instance of the 'TreeNode' class
        using the data provided.

        :param node_id: the ID value for the current 'TreeNode' instance.
        :param payload: the data carried by the 'TreeNode' instance.
        :param children: a children instance of another 'TreeNode'.
        :param parent: a parent instance of another 'TreeNode'.
        """
        self.id = node_id
        self.payload = payload
        self.children = children
        self.parent = parent

    @property
    def id(self) -> int:
        """Use this function to return the ID value for the current instance.

        This function is used for returning the node ID for the current 'TreeNode'
        instance.

        :return: the ID value for the 'TreeNode' instance.
        """
        return self._id

    @id.setter
    def id(self, new_id: int) -> None:
        """Use this function to set a new ID value for the instance.

        This function is used for setting a new node ID value for the current
        'TreeNode' instance.

        :param new_id: the new ID value.
        """
        if isinstance(new_id, int):
            self._id = new_id
        elif isinstance(new_id, float):
            print("WARNING: Converting float to integer!")
            self._id = int(new_id)
        else:
            raise TypeError(
                "New ID value for the TreeNode instance must be of type "
                "int and not: '%s'",
                type(new_id),
            )

    @property
    def payload(self) -> Any:
        """Use this function as a getter for the '_payload' attribute.

        This function is used as a getter function for the '_payload' attribute to
        allow for conditions to be applied to the attribute.

        :return: the value stored in the '_payload' variable.
        """
        return self._payload

    @payload.setter
    def payload(self, new_payload: Any) -> None:
        """Use this function to set a new payload for the current  instance.

        This function is used for updating the payload value for the current
        'TreeNode' instance.

        :param new_payload: the new payload for the current instance.
        """
        if not isinstance(new_payload, TreeNode):
            self._payload = new_payload
        else:
            raise TypeError("payload must not be of type TreeNode!")

    @property
    def children(self) -> list:
        """Use this function as a getter for the '_children' attribute.

        This function is used as a getter function for the '_children' attribute to
        allow for conditions to be applied to the attribute.

        :return: the value stored in the '_children' variable.
        """
        return self._children

    @children.setter
    def children(self, new_children: list) -> None:
        """Use this function to assign a children to the current instance.

        This function is used for setting a new children 'TreeNode' to the  current
        'TreeNode' instance.

        :param new_children: the new children 'TreeNode' to assign.
        """
        if isinstance(new_children, list):
            self._children = new_children
        elif isinstance(new_children, dict):
            self._children = [TreeNode(**child) for child in new_children]
        elif new_children is None:
            self._children = list()
        else:
            raise TypeError("Children passed could not be correctly parsed!")

    @property
    def parent(self) -> "TreeNode":
        """Use this function as a getter for the '_parent' attribute.

        This function is used as a getter function for the '_parent' attribute to
        allow for conditions to be applied to the attribute.

        :return: the value stored in the '_parent' variable.
        """
        return self._parent

    @parent.setter
    def parent(self, new_parent: "TreeNode") -> None:
        """Use this function to assign a parent to the current instance.

        This function is used for setting a new parent 'TreeNode' to the current
        TreeNode instance.

        :param new_parent: the new parent 'TreeNode' to assign.
        """
        if isinstance(new_parent, TreeNode):
            self._parent = new_parent
        elif isinstance(new_parent, dict):
            self._parent = TreeNode(**new_parent)
        elif new_parent is None:
            self._parent = None
        else:
            raise TypeError(
                "New Parent Must be of type 'TreeNode', not '{}'!".format(
                    type(new_parent)
                )
            )

    def add_child(self, new_child: "TreeNode") -> None:
        """Use this function to add another child to the list of children.

        This function is used for appending another child to the list of children for
        the current 'TreeNode' instance.

        :param new_child: the new 'TreeNode' to be added to the current instance as a
                          child.
        """
        if isinstance(new_child, TreeNode):
            self._children.append(new_child)
        else:
            raise TypeError(
                "Child must be of type 'TreeNode'! Currently of type: '%s'",
                type(new_child),
            )

    def __eq__(self, comparison: "TreeNode") -> bool:
        """Use this function to compare the current instance against another.

        This function is used to override the magic function to correctly compare the
        current 'TreeNode' instance against another to check they are the same.

        :param comparison: the other 'TreeNode' instance to compare.
        :return: whether the current instance is equal to the comparison instance.
        """
        return (
            self.id == comparison.id
            and self.payload == comparison.payload
            and self.children == comparison.children
            and self.parent == comparison.parent
        )

    def __repr__(self) -> str:
        """Use this function to create a representation of a 'TreeNode'.

        This function is used for creating a string representation of a 'TreeNode'
        instance.

        :return: a string representation of the current instance.
        """
        return "<TreeNode ID: {}, Payload: {}, Parent: {}, Child: {}>".format(
            self.id, self.payload, self.parent, self.children
        )
