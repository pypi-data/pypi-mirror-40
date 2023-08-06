# -*- coding: utf-8 -*-
"""
Module utils.py
-----------------
 A set of utility functions that are used to build resources and swagger specification.
"""
import pyparsing as pp
from simple_mappers.object_mapper import JsonObject


param_mark = pp.CaselessLiteral(":param").suppress()
return_mark = pp.Or([
    pp.CaselessLiteral(":return"),
    pp.CaselessLiteral(":returns")
]).suppress()

raise_mark = pp.Or([
    pp.CaselessLiteral(":raise"),
    pp.CaselessLiteral(":raises")
]).suppress()

consumes_mark = pp.CaselessLiteral(":consumes:")
consumes_mark = consumes_mark.suppress()
produces_mark = pp.CaselessLiteral(":produces:")
produces_mark = produces_mark.suppress()
version_mark = pp.CaselessLiteral(":version:")
version_mark = version_mark.suppress()

other_marks = pp.Or(
    [
        pp.CaselessLiteral(":arg"),
        pp.CaselessLiteral(":argument"),
        pp.CaselessLiteral(":cvar"),
        pp.CaselessLiteral(":ivar"),
        pp.CaselessLiteral(":except"),
        pp.CaselessLiteral(":exception"),
        pp.CaselessLiteral(":key"),
        pp.CaselessLiteral(":keyword"),
        pp.CaselessLiteral(":parameter"),
        pp.CaselessLiteral(":rtype"),
        pp.CaselessLiteral(":type"),
        pp.CaselessLiteral(":var"),
    ]
)

any_start_mark = pp.Or([
    param_mark,
    return_mark,
    raise_mark,
    consumes_mark,
    produces_mark,
    version_mark,
    other_marks
]).suppress()


class BaseElement(pp.ParseElementEnhance):
    """
    BaseGrammar element class.
    """
    def __init__(self, savelist=False, name=None):
        exprs = self.get_exprs()
        # super class init call.
        super().__init__(exprs, savelist)

        if name is None:
            self.setName(self.__class__.__name__.lower())
            self.setResultsName(self.__class__.__name__.lower())
        else:
            self.setName(name)
            self.setResultsName(name)


    def get_exprs(self):
        """
        Py parsing expression definition.
        :return: an expression
        """
        raise NotImplementedError("Abstract method.")

    def setName(self, name):
        """
        Define name for this expression, makes debugging and exception messages clearer.

        Example::
            Word(nums).parseString("ABC")  # -> Exception: Expected W:(0123...) (at char 0), (line:1, col:1)
            Word(nums).setName("integer").parseString("ABC")  # -> Exception: Expected integer (at char 0), (line:1, col:1)
        :param name: the name to be set.
        :return: self
        """
        self.expr = self.expr.setName(name)

        return super().setName(name)

    def setResultsName(self, name, listAllMatches=False):
        """
        Define name for referencing matching tokens as a nested attribute
        of the returned parse results.
        NOTE: this returns a *copy* of the original C{ParserElement} object;
        this is so that the client can define a basic element, such as an
        integer, and reference it in multiple places with different names.

        You can also set results names using the abbreviated syntax,
        C{expr("name")} in place of C{expr.setResultsName("name")} -
        see L{I{__call__}<__call__>}.

        Example::
            date_str = (integer.setResultsName("year") + '/'
                        + integer.setResultsName("month") + '/'
                        + integer.setResultsName("day"))

            # equivalent form:
            date_str = integer("year") + '/' + integer("month") + '/' + integer("day")
        :param name: the name to be set
        :param listAllMatches:
        :return:
        """
        self.expr = self.expr.setResultsName(name, listAllMatches)
        return super().setResultsName(name, listAllMatches)


class Param(BaseElement):
    """
    Represents a parameter in doc string.
    """
    def get_exprs(self):

        param_name = pp.Word(pp.alphanums + "_").setName("name").setResultsName("name")

        end_mark = pp.Or([
            any_start_mark.suppress(),
            pp.stringEnd
        ]).suppress()
        param_description = pp.SkipTo(end_mark) \
            .setName("description").setResultsName("description")

        return pp.Group(
            param_mark +
            param_name +
            pp.CaselessLiteral(":").suppress() +
            param_description +
            pp.FollowedBy(end_mark).suppress()
        ).setName("param").setResultsName("param")


class Raise(BaseElement):
    """
    Represents a raise doc string.
    """

    def get_exprs(self):
        error = pp.Word(pp.alphanums + "_.").setName("error").setResultsName("error")
        # error_description = pp.Word(pp.printables + " ").setName("description").setResultsName("description")
        end_mark = pp.Or([
            any_start_mark.suppress(),
            pp.stringEnd
        ]).suppress()
        error_description = pp.SkipTo(end_mark) \
            .setName("description").setResultsName("description")
        return pp.Group(
            raise_mark +
            error +
            pp.CaselessLiteral(":").suppress() +
            error_description +
            pp.FollowedBy(end_mark).suppress()
        ).setName("raise").setResultsName("raise")


class Return(BaseElement):
    """
    Represents a return/returns in doc string.
    """

    def get_exprs(self):
        end_mark = pp.Or([
            any_start_mark.suppress(),
            pp.stringEnd
        ]).suppress()
        description = pp.SkipTo(end_mark) \
            .setName("description").setResultsName("description")
        return pp.Group(
            return_mark +
            description +
            pp.FollowedBy(end_mark).suppress()
        ).setName("raise").setResultsName("raise")


class Consumes(BaseElement):
    """
    Represents a consumes in doc string.
    """

    def get_exprs(self):
        description = pp.Word(pp.printables + " ").setName("description").setResultsName("description")
        end_mark = pp.Or([
            any_start_mark.suppress(),
            pp.stringEnd
        ]).suppress()
        return pp.Group(
            consumes_mark +
            description +
            pp.FollowedBy(end_mark).suppress()
        ).setName("consumes").setResultsName("consumes")


class Produces(BaseElement):
    """
    Represents a consumes in doc string.
    """

    def get_exprs(self):
        description = pp.Word(pp.printables + " ").setName("description").setResultsName("description")
        end_mark = pp.Or([
            any_start_mark.suppress(),
            pp.stringEnd
        ]).suppress()
        return pp.Group(
            produces_mark +
            description +
            pp.FollowedBy(end_mark).suppress()
        ).setName("produces").setResultsName("produces")


class Version(BaseElement):
    """
    Represents a consumes in doc string.
    """

    def get_exprs(self):
        description = pp.Word(pp.printables + " ").setName("description").setResultsName("description")
        end_mark = pp.Or([
            any_start_mark.suppress(),
            pp.stringEnd
        ]).suppress()
        return pp.Group(
            version_mark +
            description +
            pp.FollowedBy(end_mark).suppress()
        ).setName("version").setResultsName("version")


class Other(BaseElement):
    """
    Any other possible mark not used to build swagger documentation.
    """

    def get_exprs(self):

        end_mark = pp.Or([
            any_start_mark.suppress(),
            pp.stringEnd
        ]).suppress()
        body = pp.SkipTo(end_mark) \
            .setName("description").setResultsName("description")

        return pp.Group(
            other_marks +
            body +
            pp.FollowedBy(end_mark).suppress()
        ).setName("other").setResultsName("other")



class DocString(BaseElement):
    """
    Represents a python doc string parser element.
    """
    def get_exprs(self):

        end_mark = pp.Or([
            any_start_mark.suppress(),
            pp.stringEnd
        ]).suppress()

        description = pp.SkipTo(end_mark)\
            .setName("description").setResultsName("description")

        any_doc = pp.Or([
            Param().setName("param").setResultsName("param"),
            Return().setName("return").setResultsName("return"),
            Raise().setName("raise").setResultsName("raise"),
            Consumes().setResultsName("consumes").setName("consumes"),
            Produces().setName("produces").setResultsName("produces"),
            Version().setResultsName("version").setResultsName("version"),
            Other().setResultsName("other").setResultsName("other").suppress(),
        ])
        # pp.locatedExpr()
        docString = description + \
                    pp.FollowedBy(end_mark).suppress() + \
                    pp.ZeroOrMore(any_doc).setName("attrs").setResultsName("attrs")

        return docString.setName("doc").setResultsName("doc")

    def parse(self, docstring):
        """
        Parses the given docstring.
        :param docstring: a docstring to be parsed.
        :type docstring: str
        :return: a SimpleMappers.JsonObject of form
            `
               {
                   "summary": ..., \n
                   "description": ..., \n
                   "params": {"name": "doc"}, \n
                   "returns": ..., \n
                   "consumes":...., \n
                   "produces":....,\n
                   "raises":....., \n
               }
            `
        """
        # result variables declaration
        params = dict()
        returns = None
        raises = dict()
        consumes = list()
        produces = list()
        version = None
        short_description = ""
        description = ""

        # split out the first row from the the docString
        # first row is used as short description.
        if docstring is not None:
            doc_rows = docstring.split("\n", 1)
            if len(doc_rows) > 1:
                short_description = doc_rows[0].strip(' ')
                parsed_doc = self.parseString(docstring)
            else:
                short_description = ""
                parsed_doc = self.parseString(docstring)

            description = parsed_doc.description
            for attr in parsed_doc.attrs:
                name = attr.getName().strip()
                if name == "param":
                    params[attr.name] = attr.description.strip()
                elif name == "return":
                    returns = attr.description.strip()
                elif name == "raise":
                    raises[attr.error] = attr.description.strip()
                elif name == "consumes":
                    consumes.append(attr.description.strip())
                elif name == "produces":
                    produces.append(attr.description.strip())
                elif name == "version":
                    version = attr.description.strip()

        ret = JsonObject(
            **{
                "summary": short_description,
                "description": description,
                "params": params,
                "returns": returns,
                "consumes": consumes,
                "produces": produces,
                "raises": raises,
                "version": version
            }
        )
        return ret
