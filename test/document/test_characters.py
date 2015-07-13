#!/usr/bin/env python
from StringIO import StringIO

from rtfng.utils import RTFTestCase
from rtfng.Elements import Document, StyleSheet
from rtfng.PropertySets import BorderPropertySet, ShadingPropertySet, TextPropertySet, ParagraphPropertySet
from rtfng.Renderer import Renderer
from rtfng.Styles import ParagraphStyle, TextStyle

from rtfng.document.base import TAB, LINE, RawCode
from rtfng.document.character import B, I, Inline, U, TEXT, Text
from rtfng.document.section import Section
from rtfng.document.paragraph import Paragraph

class CharacterTestCase(RTFTestCase):

    def make_charStyleOverride():
        doc, section, styles = RTFTestCase.initializeDoc()
        p = Paragraph()
        p.append('This is a standard paragraph with the default style.')
        p = Paragraph()
        p.append('It is also possible to manully override a style. ',
                  'This is a change of just the font ',
                  TEXT('size', size=48),
                  ' an this is for just the font ',
                  TEXT('typeface', font=styles.Fonts.Impact) ,
                  '.')
        section.append(p)
        return doc
    make_charStyleOverride = staticmethod(make_charStyleOverride)

    def test_charStyleOverride(self):
        self.doTest()

    def make_charColours():
        doc, section, styles = RTFTestCase.initializeDoc()
        section.append('This example test changing the colour of fonts.')
        # Text properties can be specified in two ways, either a text object
        # can have its text properties specified via the TextPropertySet
        # object, or by passing the colour parameter as a style.
        red = TextPropertySet(colour=styles.Colours.Red)
        green = TextPropertySet(colour=styles.Colours.Green)
        blue = TextPropertySet(colour=styles.Colours.Blue)
        yellow = TextPropertySet(colour=styles.Colours.Yellow)
        p = Paragraph()
        p.append('This next word should be in ')
        p.append(Text('red', red))
        p.append(', while the following should be in their respective ')
        p.append('colours: ', Text('blue ', blue), Text('green ', green))
        p.append('and ', TEXT('yellow', colour=styles.Colours.Yellow), '.')
        # When specifying colours it is important to use the colours from the
        # style sheet supplied with the document and not the StandardColours
        # object each document get its own copy of the stylesheet so that
        # changes can be made on a document by document basis without mucking
        # up other documents that might be based on the same basic stylesheet.
        section.append(p)
        return doc
    make_charColours = staticmethod(make_charColours)

    def test_charColours(self):
        self.doTest()

    def make_charUnicode():
        doc, section, styles = RTFTestCase.initializeDoc()
        section.append('This tests unicode.')
        
        p = Paragraph()
        p.append(u'32\u00B0 Fahrenheit is 0\u00B0 Celsuis')
        section.append(p)
        
        p = Paragraph()
        p.append(u'Henry \u2163 is Henry IV in unicode.')
        section.append(p)
        

        return doc
    make_charUnicode = staticmethod(make_charUnicode)

    def test_charUnicode(self):
        self.doTest()


    def make_charFrame():
        doc, section, styles = RTFTestCase.initializeDoc()
        p = Paragraph()
        thinEdge = BorderPropertySet(width=20, style=BorderPropertySet.SINGLE, colour=styles.Colours.Blue)
        textWithFrame = TextPropertySet(frame=thinEdge)
        p.append(Text('This tests frame drawn around text.', textWithFrame))
        section.append(p)
        return doc
    make_charFrame = staticmethod(make_charFrame)

    def test_charFrame(self):
        self.doTest()


    def make_charTab():
        doc, section, styles = RTFTestCase.initializeDoc()
        p = Paragraph()
        p.append('Before tab')
        p.append(Text(TAB))
        p.append('After tab')
        section.append(p)
        return doc
    make_charTab = staticmethod(make_charTab)

    def test_charTab(self):
        self.doTest()


    def make_charInline():
        doc, section, styles = RTFTestCase.initializeDoc()
        p = Paragraph()
        p.append(Inline('Simple Inline Element'))
        section.append(p)
        
        # Test various element types inside Inline element.
        p = Paragraph()
        p.append(Inline('First Inline Element',
                        TAB,
                        'Second Inline Element',
                        RawCode(r'\tab '),
                        'After tab'
                       ))
        section.append(p)
        return doc
    make_charInline = staticmethod(make_charInline)

    def test_charInline(self):
        self.doTest()




class CharacterAPITestCase(RTFTestCase):

    def test_text(self):
        t = Text()
        t = Text('abc')
        style = StyleSheet()
        normalText = TextStyle(TextPropertySet(style.Fonts.Arial, 22))
        blue = TextPropertySet(colour=style.Colours.Blue)
        shading = ShadingPropertySet()
        t = Text(normalText, blue, shading, 'abc')

    def test_textConvenience(self):
        t = TEXT('abc')
        t = TEXT('abc', 'def')

        t = B('abc')
        t = B('abc', 'def')

        t = I('abc')
        t = I('abc', 'def')

        t = U('abc')
        t = U('abc', 'def')

    def test_TextPropertySet(self):
        style = StyleSheet()
        blue = TextPropertySet(colour=style.Colours.Blue)
        red = blue.Copy()
        red.colour = style.Colours.Red
        
        # Confirm that the copies are independent objects.
        assert blue.colour == style.Colours.Blue
        assert red.colour == style.Colours.Red

    def test_ParagraphPropertySet(self):
        left = ParagraphPropertySet(ParagraphPropertySet.LEFT)
        center = left.Copy()
        center.Alignment = ParagraphPropertySet.CENTER
        
        # Confirm that the copies are independent objects.
        assert left.Alignment == ParagraphPropertySet.LEFT
        assert center.Alignment == ParagraphPropertySet.CENTER

    def test_ParagraphStyle(self):
        
        # Normal constructor.
        style = StyleSheet()
        normalText = TextStyle(TextPropertySet(style.Fonts.Arial, 22))
        ps = ParagraphStyle('Normal', normalText.Copy())
        assert ps.name == 'Normal'

        # Not sending font to constructor.
        noStyle = TextStyle(TextPropertySet())
        self.assertRaises(Exception, ParagraphStyle, 'Normal', noStyle)

        # Not sending size to constructor.
        fontOnlyStyle = TextStyle(TextPropertySet(style.Fonts.Arial))
        self.assertRaises(Exception, ParagraphStyle, 'Normal', fontOnlyStyle)

    def test_CustomElementOutsidePara(self):

        # It's just too hard to write a standard test with a custom renderer.
        doc, section, styles = RTFTestCase.initializeDoc()
        class CustomClass(object):
            pass
        section.append(CustomClass())
        
        # Define renderer with custom element support.
        specialString = "ABC I'm unique"
        def customElementWriter(renderer, element):
            renderer._write(specialString)
        r = Renderer(write_custom_element_callback=customElementWriter)
        
        # Render with custom element.
        result = StringIO()
        r.Write(doc, result)
        testData = result.getvalue()
        result.close()
        
        # Confirm generate result has custom rendering.
        assert specialString in testData

    def test_CustomElementInsidePara(self):

        # It's just too hard to write a standard test with a custom renderer.
        doc, section, styles = RTFTestCase.initializeDoc()
        p = Paragraph()
        p.append('This is a standard paragraph with the default style.')
        class CustomClass(object):
            pass
        p.append(CustomClass())
        section.append(p)
        
        # Define renderer with custom element support.
        specialString = "ABC I'm unique"
        def customElementWriter(renderer, element):
            renderer._write(specialString)
        r = Renderer(write_custom_element_callback=customElementWriter)
        
        # Render with custom element.
        result = StringIO()
        r.Write(doc, result)
        testData = result.getvalue()
        result.close()
        
        # Confirm generate result has custom rendering.
        assert specialString in testData

    def test_ExceptionOnUnknownElement(self):

        # Create document with unknown element type.
        doc, section, styles = RTFTestCase.initializeDoc()
        class CustomClass(object):
            pass
        section.append(CustomClass())
        
        # Try to render.
        r = Renderer()
        result = StringIO()
        self.assertRaises(Exception, r.Write, doc, result)

