#Author- Ela Materny
#Description- Creating rectangle or triangle or in circle 3d

import adsk.core, adsk.fusion, adsk.cam
app = adsk.core.Application.get()
ui  = app.userInterface
des = adsk.fusion.Design.cast(app.activeProduct)
root = des.rootComponent


class rectangle_trianglelogic():
    def __init__(self, des: adsk.fusion.Design):
        self.des = des

    def create_command_inputs(self, inputs: adsk.core.CommandInputs):
        self.visible_inputs = False

        self.figure = inputs.addDropDownCommandInput('figure','Select solid to create',dropDownStyle= 0)
        self.rectangle = self.figure.listItems.add('rectangle',False)
        self.triangle = self.figure.listItems.add('triangle',False)
        self.circle = self.figure.listItems.add('circle',False)

        self.inputGroup1 = inputs.addGroupCommandInput("Dim_rectangle", 'Set rectangle/triangle dimensions')
        self.inputGroup1.isVisible = self.visible_inputs
        self.rectangle1 = self.inputGroup1.children.addValueInput('value input1','Length','mm',adsk.core.ValueInput.createByReal(float(1)))
        self.rectangle2 = self.inputGroup1.children.addValueInput('value input2','Width','mm',adsk.core.ValueInput.createByReal(float(1)))
        self.rectangle3 = self.inputGroup1.children.addValueInput('value input3','Height','mm',adsk.core.ValueInput.createByReal(float(1)))

        self.inputGroup2 = inputs.addGroupCommandInput("Dim_circle", 'Set circle dimensions')
        self.inputGroup2.isVisible = self.visible_inputs
        self.circle1 = self.inputGroup2.children.addValueInput('value input4','Radius','mm',adsk.core.ValueInput.createByReal(float(1)))
        self.circle2 = self.inputGroup2.children.addValueInput('value input5','Height','mm',adsk.core.ValueInput.createByReal(float(1)))



    def handle_input_changed(self, args: adsk.core.CommandEventArgs):
        eventArgs = adsk.core.InputChangedEventArgs.cast(args)
        changedInput = eventArgs.input
        global msg
        if changedInput.id == 'figure':
            if changedInput.selectedItem.name == 'triangle':
                msg = 'triangle'
                self.inputGroup1.isVisible = True
                self.inputGroup2.isVisible = False
                self.circle1.isVisible = False
                self.circle2.isVisible = False

            elif changedInput.selectedItem.name == 'rectangle':
                msg = 'rectangle'
                self.inputGroup1.isVisible = True
                self.inputGroup2.isVisible = False
                self.circle1.isVisible = False
                self.circle2.isVisible = False

            else:
                self.inputGroup1.isVisible = False
                self.inputGroup2.isVisible = True
                self.circle1.isVisible = True
                self.circle2.isVisible = True
                msg = 'circle'



    def handle_execute(self, args: adsk.core.CommandEventArgs):
        extrudes = root.features.extrudeFeatures
        # create a sketch
        sketches = root.sketches
        sketch1 = sketches.add(root.xYConstructionPlane)
        sketchLines = sketch1.sketchCurves.sketchLines


        if msg == 'rectangle':
            #dimensions
            x = float(self.rectangle1.value)
            y = float(self.rectangle2.value)
            z = float(self.rectangle3.value)
            startPoint = adsk.core.Point3D.create(0,0,0)
            endPoint = adsk.core.Point3D.create(x/2,y/2,0)
            sketchLines.addCenterPointRectangle(startPoint,endPoint)
            sketchLines.addByTwoPoints(startPoint,endPoint)
            prof = sketch1.profiles.item(0) 
            hight = adsk.core.ValueInput.createByReal(z) 
            extrude_simple = extrudes.addSimple(prof, hight, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) 
            body_simple = extrude_simple.bodies.item(0) 
            body_simple.name = "Len.: " + str(x) + "   Wid.: " + str(z) + "  Hig.: " + str(y)

        elif msg == 'triangle':
            #dimensions
            x = float(self.rectangle1.value)
            y = float(self.rectangle2.value)
            z = float(self.rectangle3.value)
            firstPoint = adsk.core.Point3D.create(0,0,0)
            secondPoint = adsk.core.Point3D.create(0,y,0)
            thirdPoint = adsk.core.Point3D.create(x,0,0) 
            sketchLines.addByTwoPoints(firstPoint,secondPoint)
            sketchLines.addByTwoPoints(firstPoint,thirdPoint)
            sketchLines.addByTwoPoints(secondPoint,thirdPoint)
            prof = sketch1.profiles.item(0) 
            hight = adsk.core.ValueInput.createByReal(z) 
            extrude_simple = extrudes.addSimple(prof, hight, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) 
            body_simple = extrude_simple.bodies.item(0) 
            body_simple.name = "Len.: " + str(x) + "   Wid.: " + str(z) + "  Hig.: " + str(y)

        else:
            #dimensions
            x = float(self.circle1.value)
            z = float(self.circle2.value)
            sketchCircles = sketch1.sketchCurves.sketchCircles
            centerPoint = adsk.core.Point3D.create(0, 0, 0)
            sketchCircles.addByCenterRadius(centerPoint, x)        
            prof = sketch1.profiles.item(0) 
            hight = adsk.core.ValueInput.createByReal(z) 
            extrude_simple = extrudes.addSimple(prof, hight, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) 
            body_simple = extrude_simple.bodies.item(0) 
            body_simple.name = "Rad.: " + str(x) + "  Hig.: " + str(z)


        expres1 = self.rectangle1.expression
        expres2 = self.rectangle2.expression
        expres3 = self.rectangle3.expression

        msg2 = f'Your values: <br>Length: {expres1}<br>Width: {expres2}<br>Height: {expres3}'
        ui.messageBox(msg2 + '<br>You chose: ' + msg)

    def handle_validate_input(self, args: adsk.core.ValidateInputsEventArgs):
        None