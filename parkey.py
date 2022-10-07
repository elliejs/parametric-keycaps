
import cadquery as cq
from cadquery import exporters

step=19.05 # mm
gap = 0.95

#stabilizers TODO:
##########
#
# Cherry
#
##########
#stabs on <> are Y centered:
#11.938mm ?
#23.8572mm (exactly 0.94" for 2.xxU and 1.5" for 3U according to Cherry spec sheet)
#Cherry            : 2U                  :<mount> = center     , <stab> 23.86mm apart
#Cherry            : 2.25U               :<mount> = center     , <stab> 23.86mm apart
#Cherry            : 2.75U               :<mount> = center     , <stab> 23.86mm apart
#Cherry            : 3U                  :<mount> = center     , <stab> 38.07mm apart
#Signature Plastics: 6.25U space [118mm] :<mount> = center     , <stab> 50mm apart
#Cherry G80-3000   : 6.25U space [118mm] :<mount> 11.9 to right, <stab> -"- (0.5U, 3.75U 5.75U)
#                  : 6.25U space [118mm]          -"-          , 40mm    (2.1U from center)
#                  : 6.25U space [118mm]          -"-          , 42.5mm  (3U from center)
#                  : 6.5U space  [123mm] :<mount> = center     , <stab> 52.25mm apart
#Corsair           : 6.5U space  [123mm] :<mount> = center     , <stab> 52.38mm apart (2.75U)
#                  : 7U space    [133mm] :<mount> = center     , <stab> 57.15mm apart (3U)
#Cherry            : 9U space    [171mm] :<mount> = center     , <stab> 66.675mm apart (3.5U)
#-"- Commodore PC-5: 10U space   [190mm] :<mount> = center     , <stab> 66.675mm apart (3.5U)
#TODO Enter keys

##########
#
# Alps
#
##########
#                  : 2U         [37.2mm] :<mount> = center     , <stab> 27 mm apart
#                  : 2.25U      [42.0mm] :<mount> = center     , <stab> 27 mm apart
#                  : 2.75U      [51.6mm] :<mount> = center     , <stab> 41 mm apart
#                  : 3U                  :<mount> = center     , <stab> ?? mm apart
#Signature Plastics: 6.25U space [118mm] :<mount> = center     , <MXstab> 50mm apart
#Big Foot          : 7U          [133mm] :<mount> = center     , <stabs> 98 mm apart,
#                                         another switch stem mount 35mm to the right and another
#                                                               special sleeve stabilizer
#                                                               4.0-3.8mm dia 35mm to the left
#                                                               protruding 6.0 mm thru the cap bottom plane
#TaiHAo            : 7U          [133mm] :<mount> = center     , <stab> 49mm each + 55m <MX> stab each
#                  : 7U space    [133mm] :<mount> = center     , <MXstab> 57.15mm apart (3U)
#TODO Enter keys


##########
#
# Choc
#
##########
#                  : 2U         [37.2mm] :<mount> = center     , <MXstab> 24 mm apart
#                  : 2.25U      [42.0mm] :<mount> = center     , <MXstab> 24 mm apart
#                  : 2.75U      [51.6mm] :<mount> = center     , <MXstab> 24 mm apart
#                  : 3U  ??? possibly 38 mm
#Signature Plastics: 6.25U space [118mm] :<mount> = center     , <MXstab> 50 mm apart

#general keycap measures
size=step - gap

#ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
ride   =  3.0 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
sw_body= 14   #mm how much the switch requires

# our generic body values
r1=0.25 #mm base corners
r2=2    #mm top edge corners
r3=0.5  #mm top edge

r4   = 0.95 #mm stem hole edge chamfers
ribsW= 1 #mm wide

#Alps stabilizer size and position (looking from top down)
# the measured value is (2.975) 3.325 x 2.055 mm on the brown (nylon?)
# Alps stabilizer insert, it most probably had some 0.15 mm
# high rib on the 3 mm sized faces for an assured interference fit.
stab_width = 3.20   #mm
stab_length= 2.10   #mm
stab_wall  = 1.0   #mm

# the stabilizer offset on the Matias set could likely benefit from
# increasing this value for some 0.2 to 0.3 mm (-2.3mm) but it
# remains to be tested and comfirmed
stab_offset = -2.0  #mm
stab_retract= -1.2  #mm

# stem is measured as 4.5 x 2.2 mm fron an OEM Alps cap
# the  intended dimension is however offset for tight fit:
# 4.55 mm x 2.25 mm
alps_stem_width = 4.50 #mm best intentionally left free of overlap
alps_stem_length= 2.25 #mm
stem_rib   = 0.1 #mm the half offset on the two opposing sides
stem_width = alps_stem_width - stem_rib*2
stem_length= alps_stem_length - stem_rib*2
stem_rib_w1= 0.5 #mm the double rib on the longer side
stem_rib_w2= 0.8 #mm the single rib on the narrow side
stem_rib_sp= 2.5 #mm how wide to putr the ribs apart

row=1


def init(style:str):
    #"low","semilow","medium","semihigh","high"
    global o,height,wall,roundness,radius,radius2,radius3,ride,sw_body,ribsZ,ride,cave,radius_offset

    if style in ["low","semilow","medium","semihigh","high"]:
        print(style)
        if style == "low":
            height   = 5.9 #mm values that work: (5.9 (for 64 mm radius!) ) 8.6, 10.5, 11.9, 13.7
            wall     =  2   #mm how thick wall we want
            roundness= 5.8 # measureless factor: from 0 to height gives sane values, a good default is 8.5
            radius   = size + (height-roundness)*4   #mm sides radius tuned to height 8.5-0
            radius2  = 64     #mm top radius (37 or 64 mm)
            radius3  = radius2 - 14 #mm alternate top radius TODO (default is 8 or 11 mm)
            radius_offset = 1.1 #mm special case when space radius needs tweaking
            #
            #ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
            ride   =  3.0 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
            sw_body= 14   #mm how much the switch requires
            ribsZ= 0.5 #mm high (stem ribs)
            ride = ride+ribsZ
            cave = size-2*wall # "cave" is the stem hole depth

            if cave < sw_body: # fitting the upper switch body
                cave = sw_body
            o=[6,6,2,0,2,-1]

        elif style == "semilow":
            height   = 8.6 #mm values that work: (5.9 (for 64 mm radius!) ) 8.6, 10.5, 11.9, 13.7
            wall     =  2   #mm how thick wall we want
            roundness= 6.5 # measureless factor: from 0 to height gives sane values, a good default is 8.5
            radius   = size + (height-roundness)*4   #mm sides radius tuned to height 8.5-0
            radius2  = 57     #mm top radius (37 or 64 mm)
            radius3  = radius2 - 11 #mm alternate top radius TODO (default is 8 or 11 mm)
            radius_offset = 1.15 #mm special case when space radius needs tweaking
            #
            #ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
            ride   =  5.5 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
            sw_body= 14   #mm how much the switch requires
            ribsZ= 1.0 #mm high (stem ribs)
            ride = ride+ribsZ
            cave = size-2*wall # "cave" is the stem hole depth

            if cave < sw_body: # fitting the upper switch body
                cave = sw_body
            o=[7,7,3,0,3,-1]

        elif style == "medium":
            height   = 10.5 #mm values that work: (5.9 (for 64 mm radius!) ) 8.6, 10.5, 11.9, 13.7
            wall     =  2   #mm how thick wall we want
            roundness= 5.5 # measureless factor: from 0 to height gives sane values, a good default is 8.5
            radius   = size + (height-roundness)*4   #mm sides radius tuned to height 8.5-0
            radius2  = 47     #mm top radius (37 or 64 mm)
            radius3  = radius2 - 8 #mm alternate top radius TODO (default is 8 or 11 mm)
            radius_offset = 1.15 #mm special case when space radius needs tweaking
            #
            #ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
            ride   =  5.5 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
            sw_body= 14   #mm how much the switch requires
            ribsZ= 1.0 #mm high (stem ribs)
            ride = ride+ribsZ
            cave = size-2*wall # "cave" is the stem hole depth

            if cave < sw_body: # fitting the upper switch body
                cave = sw_body
            o=[7,7,4,0,4,-1]

        elif style == "semihigh":
            height   = 11.9 #mm values that work: (5.9 (for 64 mm radius!) ) 8.6, 10.5, 11.9, 13.7
            wall     =  2   #mm how thick wall we want
            roundness= 5.5 # measureless factor: from 0 to height gives sane values, a good default is 8.5
            radius   = size + (height-roundness)*4   #mm sides radius tuned to height 8.5-0
            radius2  = 37    #mm top radius (37 or 64 mm)
            radius3  = radius2 - 11 #mm alternate top radius TODO (default is 8 or 11 mm)
            radius_offset = 1.2 #mm special case when space radius needs tweaking
            #
            #ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
            ride   =  5.5 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
            sw_body= 14   #mm how much the switch requires
            ribsZ= 1.5 #mm high (stem ribs)
            ride = ride+ribsZ
            cave = size-2*wall # "cave" is the stem hole depth

            if cave < sw_body: # fitting the upper switch body
                cave = sw_body
            o=[8,8,4,0,4,-1]

        elif style == "high":
            height   = 13.7 #mm values that work: (5.9 (for 64 mm radius!) ) 8.6, 10.5, 11.9, 13.7
            wall     =  2   #mm how thick wall we want
            roundness= 4.5 # measureless factor: from 0 to height gives sane values, a good default is 8.5
            radius   = size + (height-roundness)*4   #mm sides radius tuned to height 8.5-0
            radius2  = 32     #mm top radius (37 or 64 mm)
            radius3  = radius2 - 11 #mm alternate top radius TODO (default is 8 or 11 mm)
            radius_offset = 1.2 #mm special case when space radius needs tweaking
            #
            #ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
            ride   =  5.5 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
            sw_body= 14   #mm how much the switch requires
            ribsZ= 2 #mm high (stem ribs)
            ride = ride+ribsZ
            cave = size-2*wall # "cave" is the stem hole depth

            if cave < sw_body: # fitting the upper switch body
                cave = sw_body
            o=[8,8,4,0,4,-1]

    else:
        #generic shape parameters:
        height   = 8.6 #mm values that work: (5.9 (for 64 mm radius!) ) 8.6, 10.5, 11.9, 13.7
        wall     =  2   #mm how thick wall we want
        roundness= 4.5 # measureless factor: from 0 to height gives sane values, a good default is 8.5
        radius   = size + (height-roundness)*4   #mm sides radius tuned to height 8.5-0
        radius2  = 57     #mm top radius (37 or 64 mm)
        radius3  = radius2 - 8 #mm alternate top radius TODO (default is 8 or 11 mm)
        radius_offset = 1.15 #mm special case when space radius needs tweaking
        #
        #ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
        ride   =  5.5 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
        sw_body= 14   #mm how much the switch requires
        ribsZ= 1.0 #mm high (stem ribs)
        ride = ride+ribsZ
        cave = size-2*wall # "cave" is the stem hole depth

        if cave < sw_body: # fitting the upper switch body
            cave = sw_body
        # calculated values for row stamping offsets:
        # -1 is special case of space row profile
        o=[7,7,4,0,4,-1]
    return

def alpsstem(dims):
    width,length=dims

    #shape the stem in positive form

    #move away along the longer side for a start
    alps_stem=cq.Workplane(origin=(-1.0,stem_width/2,0))
    #we start drawing the narrow side from the corner:
    alps_stem=alps_stem.line((stem_length-stem_rib_w2)/2, 0  )
    #the ribs are ADDED to the stem size:
    alps_stem=alps_stem.line(0  , stem_rib)
    alps_stem=alps_stem.line(stem_rib_w2, 0  )
    alps_stem=alps_stem.line(0  ,-stem_rib)
    alps_stem=alps_stem.line((stem_length-stem_rib_w2)/2, 0  )
    alps_stem=alps_stem.line(0  ,-stem_rib)
    #wider side next:
    alps_stem=alps_stem.line(   0,-(stem_width-stem_rib_sp-stem_rib_w1*2)/2 )
    alps_stem=alps_stem.line( stem_rib, 0  )
    alps_stem=alps_stem.line(   0,-stem_rib_w1 )
    alps_stem=alps_stem.line(-stem_rib, 0  )
    # we use defined rib spacing and are hardcoed for 2 ribs only
    alps_stem=alps_stem.line(   0,-stem_rib_sp)
    alps_stem=alps_stem.line( stem_rib, 0  )
    alps_stem=alps_stem.line(   0,-stem_rib_w1 )
    alps_stem=alps_stem.line(-stem_rib, 0  )
    alps_stem=alps_stem.line(   0,-(stem_width-stem_rib_sp-stem_rib_w1*2)/2 )
    #and a corner and back to the other narrow side:
    alps_stem=alps_stem.line(-(stem_length-stem_rib_w2)/2, 0  )
    alps_stem=alps_stem.line(0  ,-stem_rib)
    alps_stem=alps_stem.line(-stem_rib_w2, 0  )
    alps_stem=alps_stem.line(0  , stem_rib)
    alps_stem=alps_stem.line(-(stem_length-stem_rib_w2)/2, 0  )
    alps_stem=alps_stem.line(0  , stem_rib)
    #and another wider side:
    alps_stem=alps_stem.line(   0, (stem_width-stem_rib_sp-stem_rib_w1*2)/2 )
    alps_stem=alps_stem.line(-stem_rib, 0  )
    alps_stem=alps_stem.line(   0, stem_rib_w1 )
    alps_stem=alps_stem.line( stem_rib, 0  )
    alps_stem=alps_stem.line(   0, stem_rib_sp)
    alps_stem=alps_stem.line(-stem_rib, 0  )
    alps_stem=alps_stem.line(   0, stem_rib_w1 )
    alps_stem=alps_stem.line( stem_rib, 0  )
    alps_stem=alps_stem.line(   0, (stem_width-stem_rib_sp-stem_rib_w1*2)/2 )
    alps_stem=alps_stem.close()
    # Alps stem is ideally flush with the keycap bottom
    alps_stem=alps_stem.extrude(ride+2.1)
    #alps_stem=alps_stem.union(ribs)

    return alps_stem

def alpsstab(dims):
    width,length=dims

    alps_stab=cq.Workplane(origin=(stab_offset,0,stab_retract+ribsZ/2+r4))
    alps_stab=alps_stab.rect(stab_width+2*stab_wall,stab_length+2*stab_wall)
    alps_stab=alps_stab.clean()
    alps_stab=alps_stab.extrude(ride+ribsZ+r4)
    #alps_stab=alps_stab.union(ribs)

    alps_stab_hole=cq.Workplane(origin=(stab_offset,0,-2))
    alps_stab_hole=alps_stab_hole.rect(stab_width,stab_length)
    alps_stab_hole=alps_stab_hole.extrude(ride+ribsZ/2+r4+2)
    alps_stab=alps_stab.cut(alps_stab_hole)
    return alps_stab

def chocv1stem(dims):
    width,length=dims
    correction= 0.025          #mm
    stemX     = 1.2-correction #mm
    stemfree  = 0.8            #mm
    stemY     = 3.0-correction #mm
    apartX    = 5.7/2          #mm
    apartY    = stemY/2-stemfree/2

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2+r4))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave+(step*(length-1)),ribsW,ribsZ)

    stem=cq.Workplane(origin=(0,0,-1))
    stem=stem.pushPoints([(apartY,apartX),(-apartY,apartX),(-apartY,-apartX),(apartY,-apartX)])
    stem=stem.rect(stemfree,stemX)
    stem=stem.pushPoints([(0,apartX),(0,-apartX)])
    stem=stem.rect(stemY,stemfree)
    stem=stem.extrude(ride+1+2.50) # this is fixed length
    stem=stem.union(ribs)

    return stem

def mxstem(dims):
    width,length=dims
    #this very MX stem is tested so far to fit:
    # Kailh ChocV2,
    # Kailh BOX (square)
    # Kailh Silent BOX (round stem)
    # Cherry MX "+" like stem

    mx_stem=cq.Workplane(origin=(0,0,-1))
    mx_stem=mx_stem.circle(2.75) # this is fixed value
    mx_stem=mx_stem.clean()
    mx_stem=mx_stem.extrude(ride+3.1) # this is fixed length
    #my stem size fixes for FDM (a smidge too tight)
    mx_stem_hole=cq.Workplane(origin=(0,0,-2))
    mx_stem_hole=mx_stem_hole.rect(4.15-0.05, 1.27+0.05)
    mx_stem_hole=mx_stem_hole.rect(1.12+0.05, 4.15-0.05)
    mx_stem_hole=mx_stem_hole.extrude(ride+2.95) # +2 mm to just be on the safe side here
    mx_stem=mx_stem.cut(mx_stem_hole)
    return mx_stem

def alps_hole (ride,dims):
    width,length=dims

    rotation=-90
    if width == 1 and length >1.75:
        rotation=0
        width = length
        length = 1

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2+r4))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave+(step*(length-1)),ribsW,ribsZ)

    #shape the stem in positive form
    alps_stem=alpsstem(dims)

    #add Alps stab stems:
    alps_stab=alpsstab(dims)
    #TODO

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave+(step*(length-1)),cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(ribs)
    hole = hole.cut(alps_stem)

    #add stabilizers
    spacing = 0
    if width == 7 or width == 6.25: # space keys:
        spacing = 98 #mm
    elif width == 2.75 or width == 3: # where will you find 3U stabilizer wire anyway?
        spacing = 41 #mm
    elif width == 2.25 or width == 2:
        spacing = 27 #mm
    if spacing != 0:
        hole=hole.cut(alps_stab.translate([0,spacing/2,0]))
        hole=hole.cut(alps_stab.translate([0,-spacing/2,0]))

    #TODO add the 35mm offset 4mm dia stabilizer axle too
    #TODO add the 35mm 2nd alps stem to 7U space bar

    return hole.rotate((0,0,0),(0,0,1),rotation)

def alpsmx_hole (ride,dims):
    width,length=dims

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2+r4))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave+(step*(length-1)),ribsW,ribsZ)

    #shape the stem in positive form
    alps_stem=alpsstem(dims)

    #MX stab stems:
    mx_stem=mxstem(dims)

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave+(step*(length-1)),cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(ribs)
    hole = hole.cut(alps_stem)

    #add stabilizers:
    spacing = 0
    if width > 2.75: # space keys:
        spacing = ( width - 1 ) * 3/4 * 25.38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing=15/16 * 25.38 #mm ( it's 3/4" x 5/4 ( 2.25U - (2 x 1/2U)) exactly )
    if spacing != 0:
        mx_stab=mx_stem.translate([0,spacing/2,0])
        hole=hole.cut(mx_stab)
        mx_stab=mx_stem.translate([0,-spacing/2,0])
        hole=hole.cut(mx_stab)
    return hole.rotate((0,0,0),(0,0,1),90)

def chocv1_hole (ride,dims):
    width,length=dims

    rotation=-90
    if width == 1 and length >1.75:
        rotation=0
        width = length
        length = 1

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2+r4))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave+(step*(length-1)),ribsW,ribsZ)

    #shape the stem in positive form
    stem=chocv1stem(dims)
    mx_stem=mxstem(dims)
    offset = 0.65 #mm Choc stem stabilizer offset

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave+(step*(length-1)),cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(ribs)
    hole = hole.cut(stem)

    #add stabilizers:
    spacing = 0
    if width >= 6.25: # space keys:
        spacing = 50 #mm
    if width > 2.75: # space keys:
        spacing = 38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing= 24 #mm
    if spacing != 0:
        mx_stab=mx_stem.translate([offset,spacing/2,0])
        hole=hole.cut(mx_stab)
        mx_stab=mx_stem.translate([offset,-spacing/2,0])
        hole=hole.cut(mx_stab)
    return hole.rotate((0,0,0),(0,0,1),rotation)

def mx_hole (ride,dims):
    width,length=dims

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2+r4))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave+(step*(length-1)),ribsW,ribsZ)

    #shape the stem in positive form
    mx_stem=mxstem(dims)

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave+(step*(length-1)),cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(ribs)
    hole = hole.cut(mx_stem)

    #add stabilizers:
    spacing = 0
    if width > 2.75: # space keys:
        spacing = ( width - 1 ) * 3/4 * 25.38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing=15/16 * 25.38 #mm ( it's 3/4" x 5/4 ( 2.25U - (2 x 1/2U)) exactly )
    if spacing != 0:
        mx_stab=mx_stem.translate([0,spacing/2,0])
        hole=hole.cut(mx_stab)
        mx_stab=mx_stem.translate([0,-spacing/2,0])
        hole=hole.cut(mx_stab)
    return hole.rotate((0,0,0),(0,0,1),90)

def topstamp (width,length,stamp_radius):
    #width=1.25
    #length=2

    #TODO:
    #  account for sub 1U sized keycaps one day maybe

    if width == 1 and length == 1:
        #we have a plain 1U key:
        stamp = cq.Workplane("front",origin=(0,0,0))
        stamp = stamp.sphere(stamp_radius)
        # rotate the spere so the seam is more favorably placed upun the body
        stamp = stamp.rotate([0,0,0],[1,0,0],90)
    elif length == 1:
        #we have an 1U long but wider key
        stamp = cq.Workplane("front",origin=(0,0,0))
        stamp = stamp.move((width-1)*step/2+stamp_radius,0)
        stamp = stamp.radiusArc(endPoint=((width-1)*step/2,-stamp_radius),radius=stamp_radius)
        stamp = stamp.line(-(width-1)*step,0)
        stamp = stamp.radiusArc(endPoint=(-(width-1)*step/2-stamp_radius,0),radius=stamp_radius)
        stamp = stamp.wire()
        stamp = stamp.revolve(0,[0,0,0],[1,0,0])
        #stamp = stamp.rotate((0,0,0),(0,0,1),90)
    elif width == 1:
        #we have a 1U narrow but longer key
        stamp = cq.Workplane("front",origin=(0,0,0))
        stamp = stamp.move((length-1)*step/2+stamp_radius,0)
        stamp = stamp.radiusArc(endPoint=((length-1)*step/2,-stamp_radius),radius=stamp_radius)
        stamp = stamp.line(-(length-1)*step,0)
        stamp = stamp.radiusArc(endPoint=(-(length-1)*step/2-stamp_radius,0),radius=stamp_radius)
        stamp = stamp.wire()
        stamp = stamp.revolve(0,[0,0,0],[1,0,0])
        #and just rotate for lenghtwise application
        stamp = stamp.rotate((0,0,0),(0,0,1),90)
    else:
        # we have a sizeable keycap here
        stamp = cq.Workplane("XY",origin=(0,0,-stamp_radius))
        stamp = stamp.rect((length-1)/2*step,(width-1)/2*step)
        stamp = stamp.offset2D(stamp_radius)
        stamp = stamp.extrude(stamp_radius*2+.01)
        stamp = stamp.edges('not( |Z )')
        stamp = stamp.fillet(stamp_radius)
    return stamp

def spherical_cap (stem,row,dims):
    width,length=dims

    cap_radius = radius2
    if row < -1: #negative means accented (except -1)
        cap_radius = radius3
        row = abs(row)

    if width > .75:
        o1=o[row]
        #preparing the forming shapes:
        stamp = topstamp (width,length,cap_radius)

        if o1 != -1: # are we convex? -1 is convex dead center
            stamp = stamp.translate([0,o1,height+cap_radius]) # slide as per row offset
        else:
            stamp = stamp.translate([0,0,height*radius_offset-cap_radius])  # we are, put it dead on center

        #the base containing shape
        cube = cq.Workplane(origin=(0,0,-size*.1))
        cube = cube.box(size*width,size*length,size*.2)

        #the bottom forming shape
        base = cq.Workplane(origin=(0,0,-step))
        # we want go high because sculpt is measured
        # from the dish lowest point -
        # we need enough material at the rim
        base = base.box(step*width,step*length,step*2.25)

        #single rounded side
        side = cq.Workplane("bottom",origin=(size/2-radius,0))
        side = side.cylinder(height=step*(width+0),radius=radius,angle=90,combine=True)
        side1 = cq.Workplane("bottom",origin=(size/2-radius,0))
        side1= side1.cylinder(height=step*(length+0),radius=radius,angle=90,combine=True)

        #two opposing sides fused:
        if length !=1:
            side2 =  side.intersect(base.rotate((0,0,0),(0,0,1),90).translate([0,0,height*1.35]))
            side2 = side2.intersect(base.rotate((0,0,0),(0,0,1),90).translate([0,0,height*1.35])) # half side profile
            side2 = side2.translate([ ((length-1)*step/2) , 0 , 0 ])
            sides = side2.rotate((0,0,0),(0,0,1),180)
            sides = sides.union(side2)
        else:
            sides = side.rotate((0,0,0),(0,0,1),180)
            sides = sides.intersect(side)
        sides = sides.rotate((0,0,0),(0,0,1),90)

        #two opposing sides at switch width distance
        sides_L = side1
        sides_L = sides_L.intersect(base.translate([step/2,0,step*1.35])) # half side profile
        sides_L = sides_L.translate([ ((width-1)*step/2) , 0 , 0 ])
        sides_R = sides_L.rotate((0,0,0),(0,0,1),180)
        #sides length wise:
        sides_LW= sides_L.union(sides_R)
        #are we wider than 1U?
        if width != 1.0: # for non unit size switchs
            sides_LW= sides_LW.box((width-1)*step,(length)*step*1.1,step*2) #we can't draw 0 width box
            #with (width-1) we are certainly clear the end of the side profiles
        sides_LW= sides_LW.intersect(base.translate([0,0,step*1]),clean=True)

        #fuse opposing sides to form a square
        form  = sides_LW
        sides = sides.rotate((0,0,0),(0,0,1),0.05)
        form  = form.intersect(sides)

        #
        # fillet sides
        #
        e_selection='not( #Z )'
        d = form.edges(e_selection)
        d = d.fillet(r2)
        form = form.edges(e_selection) # we are pencil (or rocket) shaped
        form = form.fillet(r2)

        #o1 = -1 is space row
        if o1 != -1: # we are digging out a conqave shape:
            stamp_offset=[0,0,0]
            shape = stamp.translate(stamp_offset)
            stamp = stamp.rotate((0,0,0),(0,0,1),-0.05)
            form = form.cut(stamp)
        else: # we are building a convex shape:
            stamp_offset=[0,0,height*4]
            stamp = stamp.rotate((0,0,0),(0,0,1),-0.05)
            shape = base.translate(stamp_offset).cut(stamp)
            form = form.cut(shape,clean=True)

        # special case for row 4 (before we cut the switch hole)
        if row == 4:
            form = form.rotate((0,0,0),(0,0,1),180)
            log("rotated :180")
        #
        # fillet top
        #
        f_select_top = '%SPHERE or ( %CYLINDER exc (<X or >X or <Y or >Y) )'
        e_select_top = 'not( %CIRCLE )'
        d = form#.faces(f_select_top).edges(e_select_top)
        #d = d.fillet(r3)
        #d = form.edges(e_select_top)
        form = form.faces(f_select_top).edges(e_select_top)

        form = form.fillet(r3)
        #width
        if width > 0:
            form = form.cut(base)
        if stem in ["","MX","mx"]:
            form = form.cut(mx_hole(ride,(width,length)))
        elif stem in ["Alps","ALPS","alps"]:
            form = form.cut(alps_hole(ride,(width,length)))
        elif stem in ["AlpsMX","ALPSMX","alpsmx"]:
            form = form.cut(alpsmx_hole(ride,(width,length)))
        elif stem in ["ChocV1","V1","chocv1","Choc","choc"]:
            form = form.cut(chocv1_hole(ride,(width,length)))
        #form = form.rotate((0,0,0),(0,0,1),90)

    #    return sides.rotate((0,0,0),(0,0,1),90).intersect(sides_LW)
    else:
        form = cq.Workplane()
    return form

#TODO:
# pick sets of values across variables and make keyset presets

init('medium') # default (none) style
#
#"low"
#
#  a most low profile specially suited for Kailh Choc V1 and V2 switches
#  (depending on tems used)
#
#"semilow"
#
#  an down to the floor profile somewhat reminiscent to the Cherry profile
#  but with spherical tops
#
#"medium"
#
#  an mid way profile for quick typing well suited for most switches
#
#"semihigh"
#
#  an traditional and serious profile
#
#"high"
#
#  an SA lookalike profile for tightly moving switches like Kailh BOX



#selection='( <Z or |X or |Y )'
init('semilow')
result = spherical_cap ("Alps",1,(2.25,1)).translate((0,0,0))
show_object(result)
keyname='semilow_Alps_R1_W2.25'
exporters.export(
    result,
    keyname+'_parkey.stl',
    tolerance=0.15,
    angularTolerance=0.125
    )

init('medium')
result = spherical_cap ("Alps",1,(2.25,1)).translate((0,step,0))
show_object(result)
keyname='medium_Alps_R1_W2.25'
exporters.export(
    result,
    keyname+'_parkey.stl',
    tolerance=0.15,
    angularTolerance=0.125
    )

init('semihigh')
result = spherical_cap ("Alps",1,(2.25,1)).translate((0,step*2,0))
show_object(result)
keyname='semihigh_Alps_R1_W2.25'
exporters.export(
    result,
    keyname+'_parkey.stl',
    tolerance=0.15,
    angularTolerance=0.125
    )

init('high')
result = spherical_cap ("Alps",1,(2.25,1)).translate((0,step*3,0))
show_object(result)
keyname='high_Alps_R1_W2.25'
exporters.export(
    result,
    keyname+'_parkey.stl',
    tolerance=0.15,
    angularTolerance=0.125
    )


#result = mx_hole (5,1.25)
#highlight = result.edges(selection)

#show_object(result, name="body", options={cq.Color("blue")})
#debug(highlight)

'''
#show a lot:
y=0
x=0
l=0


for s in [(1,2),(1.25,1),(1.5,1.5),(1.75,1),(2.0,1),(1,1)]:
    sx,sy=s
    y=y+(sx+l)/2
    x=0
    for k in range(0,5):
        x=x+sy
        r = k+1 #row
        result = spherical_cap ("choc",r,s).translate ([y*step,(x-(sy/2))*step,0])
        show_object(result)
    l=sx
'''

# sculpt, width
#a MIT planck:
keybrd = [
#    [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]],
    [[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]],
    [[2,1],[2,1],[2,1],[2,1],[-2,1],[2,1],[2,1],[-2,1],[2,1],[2,1],[2,1],[2,1]],
    [[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1]],
#    [[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1]],
    [[4,1],[4,1],[4,1],[4,1],[5,1],[5,2],[5,0],[5,1],[4,1],[4,1],[4,1],[4,1]],
    ]


'''
#ANSI 60%
keybrd = [
  [[1,1],[1,1],[0,.75],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,2],[1,0],[0,.75],[1,1],[1,1.5],[1,1.5]],
  [[2,1],[2,1],[0,.75],[2,1.5],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1.5],[2,0],[0,.75],[2,1],[2,1],[2,1],[2,1]],
  [[3,1],[3,1],[0,.75],[3,1.75],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,2.25],[3,0],[3,0],[0,.75],[3,1],[3,1],[3,1],[3,1]],
  [[4,1],[4,1],[0,.75],[4,2.25],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,2.75],[4,0],[4,0],[4,0],[0,.75],[4,1],[4,1],[4,1],[4,1]],
  [[4,1],[4,1],[0,.75],[4,1.25],[4,1.25],[4,1.25],[5,6.25],[4,0],[4,0],[4,0],[4,0],[4,0],[4,0],[4,0],[4,1.25],[4,1.25],[4,1.25],[4,1.25],[5,.75],[4,2],[4,1],[4,1]],
  ]

'''
'''
a=0
b=0
for x in range(len(keybrd)):
    a=a+1
    log(b)
    b=0
    for y in range(len(keybrd[x])):
        t="Choc"
        s=keybrd[x][y][0]
        w=keybrd[x][y][1]
        b=b+w/2
        result = spherical_cap(t,s,(w,1)).translate([-b*19.05,a*19.05,0])
        b=b+w/2
        show_object(result,options={cq.Color("blue")})
'''
'''
exporters.export(
    result,
    keyname+'parkey.stl',
    tolerance=0.15,
    angularTolerance=0.125
    )

exporters.export(
    result,
    'SA_keyset.svg',
    opt={
        "width": 300,
        "height": 300,
        "marginLeft": 40,
        "marginTop": 40,
        "showAxes": True,
        "projectionDir": (0.5, -0.5, 1),
        "strokeWidth": 0.25,
        "strokeColor": (255, 0, 0),
        "hiddenColor": (0, 0, 255),
        "showHidden": True,
        },
    )
'''
