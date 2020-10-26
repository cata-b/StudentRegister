from Domain.BaseID import BaseID
from Domain.CustomErrors import *
from Domain.IDListAction import IDListAction
from difflib import get_close_matches
from copy import deepcopy

class BaseIDList(object):

    """
    Class for representing a list of objects that inherit from BaseID (but one type per list).
    """

    def __init__(self):
        self._content = {}
        self._query_result = []
        self._orderbyattr = "ID"
        self._filterbyattr = "ID"
        self._filtervalue = 0
        self._strictfilter = False
        self._desc_order = False
        self._undo_list = []
        self._redo_list = []
        self._latest_ID = 0

    def __sort_query_result(self):
        """
        ShellSort with an inner binary insertion sort for sorting the query result by the OrderAttribute, set by calling SetQueryOptions
        """
        def search(list, start, end, gap, what):
            if abs(start - end) <= gap:
                if what < getattr(self._content[list[start]], self._orderbyattr):
                    return start
                else: 
                    return end
            middle = (((start + end) // 2) - start) // gap * gap + start
            if getattr(self._content[list[middle]], self._orderbyattr) > what:
                return search(list, start, middle, gap, what)
            else:
                return search(list, middle, end, gap, what)
        list = self._query_result
        n = len(list)
        gap = n - 1
        while gap > 0:
            start = 0
            for i in range(gap, n, 1):
                if getattr(self._content[list[i - gap]], self._orderbyattr) > getattr(self._content[list[i]], self._orderbyattr):
                    pos = search(list, start, i - gap, gap, getattr(self._content[list[i]], self._orderbyattr))
                    temp = list[i]
                    for j in range(i, pos, -gap):
                        list[j] = list[j - gap]
                    list[pos] = temp
                start = (start + 1) % gap
            gap //= 2
        
    def __get_query_result(self):
        """
        Method for obtaining the query result in self.__query_result, respecting conditions set using SetQueryOptions.
        Query is lazy loaded, so this method will be called when query is needed.
        """
        self._query_result = []
        if len(self._content) == 0:
            return
        if self._filterbyattr != None and self._filtervalue != None:
            if not self._strictfilter:
                search_list = []
                for item in list(self._content.values()):
                    search_list.append(str(getattr(item, self._filterbyattr)).lower())
                search_list = list(set(get_close_matches(str(self._filtervalue.lower()), search_list)))
                for item in list(self._content.values()):
                    for found in search_list:
                        if str(getattr(item, self._filterbyattr)).lower() == found:
                            self._query_result.append(item.ID)
            else:
                for item in list(self._content.values()):
                    if str(getattr(item, self._filterbyattr)) == self._filtervalue:
                        self._query_result.append(item.ID)
        else:
            for item in list(self._content.values()):
                self._query_result.append(item.ID)
        if self._orderbyattr == "ID":
            self._query_result = sorted(self._query_result)
        elif self._orderbyattr != None:
            self.__sort_query_result()
            #for i in range(len(self._query_result)):
            #    for j in range(i + 1, len(self._query_result)):
            #        if getattr(self._content[self._query_result[i]], self._orderbyattr) > getattr(self._content[self._query_result[j]], self._orderbyattr):
            #            self._query_result[i], self._query_result[j] = self._query_result[j], self._query_result[i]
            if self._desc_order:
                    self._query_result.reverse()

    def __getitem__(self, key_query):
        """
        Method for the indexing operator.
        parameters: 
            - key(int) the ID to search for, or, in case query is set to True, the key-th item from the query
            - query(bool) (default false) 
        output:
            - a BaseID instance
        """
        key = None
        ordered = False
        if isinstance(key_query, tuple):
            key, ordered = key_query
        else:
            key = key_query
        if not isinstance(key, int) or not isinstance(ordered, bool):
            raise InvalidParametersError("Parameters should be int, bool")
        if ordered:
            if len(self._query_result) == 0:
                self.__get_query_result()
            return self._content[self._query_result[key]]
        else:
            if not self.HasKey(key):
                raise NonExistentItemIDError("ID does not exist.")
            return self._content[key]

    def Length(self, Query=False):
        """
        Gets length of the list or of the query if Query = True
        parameters: Query - bool
        output: int
        """
        if Query:
            if len(self._query_result) == 0:
                self.__get_query_result()
            return len(self._query_result)
        return len(self._content)

    def HasKey(self, key):
        """
        Checks whether ID already exists in the list.
        parameters: key(int)
        output: bool
        """
        if not isinstance(key, int):
            raise InvalidParametersError("Parameter should be int.")
        return (key in self._content.keys())

    def GetSafeKey(self):
        """
        Gets an ID value that is guaranteed to be safe (that is, it never existed in the list)
        parameters: -
        returns: int
        """
        return self._latest_ID + 1

    @property
    def IDs(self):
        return sorted(list(self._content.keys()))

    @property
    def QueryIDs(self):
        if len(self._query_result) == 0:
            self.__get_query_result()
        return self._query_result

    def SetQueryOptions(self, FilterAttribute="ID", FilterValue=0, StrictFilter=False, OrderAttribute="ID", Descending=False):
        """
        Sets query options that will be used to make the query.
        parameters:
            - FilterAttribute(str or None): the name of the attribute to search for
            - FilterValue(object or None): the value that attribute should have
            - StrictFilter(bool or None): whether matches will be close or equal
            - OrderAttribute(str or None): the name of the attribute to sort by
            - Descending(bool): whether result is in descending or ascending order
        output: None
        exceptions:
            - InvalidParametersError if any of the parameters' types are off.
        """
        if not (isinstance(FilterAttribute, str) or FilterAttribute == None) or not (isinstance(OrderAttribute, str) or OrderAttribute == None) or not isinstance(Descending, bool) or not (isinstance(StrictFilter, bool) or StrictFilter == None):
            raise InvalidParametersError("Parameters should be str, object, str, bool.")
        self._filterbyattr = FilterAttribute
        self._filtervalue = str(FilterValue)
        self._orderbyattr = OrderAttribute
        self._desc_order = Descending
        self._query_result = []
        self._strictfilter = StrictFilter

    def AddItems(self, items):
        """
        Adds a (python) list of items to the BaseIDList.
        parameters:
            - items: list
        output: None
        exceptions:
            - InvalidParametersError if any of the items in the list is of different type than what is already in the BaseIDList instance.
            - IDExistsError if any of the items in the list has the ID already in the BaseIDList instance.
        """
        added_items = []
        for item in items:
            if not isinstance(item, BaseID):
                raise InvalidParametersError("Parameter should be a BaseID instance.")
            if len(self._content) > 0:
                if type(list(self._content.values())[0]) != type(item):
                    raise InvalidParametersError("Parameter should be a " + str(type(list(self._content.values())[0])) + " instance.")
            if item.ID in self._content:
                raise IDExistsError("ID already exists in the list.")
            if item.ID > self._latest_ID:
                self._latest_ID = item.ID
            self._content[item.ID] = item
            added_items.append(deepcopy(item))
        self._undo_list.append(IDListAction(IDListAction.AddAction, added_items))
        self._redo_list.clear()
        self._query_result = None
    
    def RemoveItems(self, itemIDs):
        """
        Removes a range of items from the BaseIDList.
        parameters:
            - itemIDs: list of int
        output: None
        remark: does not raise exceptions if IDs are non-existent
        """
        removed_items = []
        for itemID in itemIDs:
            if itemID in self._content.keys():
                removed_items.append(self._content[itemID])
                del self._content[itemID]
        self._undo_list.append(IDListAction(IDListAction.RemoveAction, removed_items))
        self._redo_list = []
        self._query_result = []

    def UpdateItem(self, itemID, new_value):
        """
        Updates an item in the BaseIDList.
        parameters:
            - itemID: int
            - new_value: BaseID
        output: None
        exceptions: InvalidParametersError if new_value is of different type than what is already in the BaseIDList.
        remark: Does not raise exceptions if itemID is not in the list
        """
        if not isinstance(new_value, type(list(self._content.values())[0])):
            raise InvalidParametersError("Cannot add different type items to the same list.")
        if self.HasKey(itemID):
            self._undo_list.append(IDListAction(IDListAction.UpdateAction, [self._content[itemID]]))
            self._redo_list = []
            new_value.ID = itemID
            self._content[itemID] = new_value

    def _reverse_action(self, action, destlist):
        """
        Reverses action stored in the 'action' param and adds its reverse to 'destlist'.
        parameters:
            - action: IDListAction
            - destlist: list
        """
        self._query_result = []
        if action.Type == IDListAction.AddAction:
            for item in action.Items:
                del self._content[item.ID]
            destlist.append(IDListAction(IDListAction.RemoveAction, action.Items))
        elif action.Type == IDListAction.RemoveAction:
            for item in action.Items:
                self._content[item.ID] = item
            destlist.append(IDListAction(IDListAction.AddAction, deepcopy(action.Items)))
        elif action.Type == IDListAction.UpdateAction:
            old_items = []
            for item in action.Items:
                old_items.append(self._content[item.ID])
                self._content[item.ID] = item
            destlist.append(IDListAction(IDListAction.UpdateAction, old_items))

    def Undo(self):
        """
        Undoes the last performed operation on the list.
        """
        if len(self._undo_list) == 0:
            raise NoMoreStepsError("No more undos.")
        self._reverse_action(self._undo_list.pop(), self._redo_list)
        self._query_result = []
    
    def Redo(self):
        """
        Redoes the last undone operation on the list.
        """
        if (len(self._redo_list)) == 0:
            raise NoMoreStepsError("No more redos.")
        self._reverse_action(self._redo_list.pop(), self._undo_list)
        self._query_result = []

