# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops, ImageFilter
import PIL.ImageOps
import numpy as np

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):

        # Solve 2x2 Problems
        if problem.problemType == "2x2":
            return self.twoByTwoAnalysis(problem)

        if problem.problemType == "3x3":
            return self.threeByThreeAnalysis(problem)

        # elif problem.problemType == "3x3":
        #     a = Image.open(problem.figures['A'].visualFilename)
        #     b = Image.open(problem.figures['B'].visualFilename)
        #
        #     # a = convert_to_blk_white(np.array(a))
        #     # b = convert_to_blk_white(np.array(b))
        #     a = np.array(a)
        #     b = np.array(b)
        #
        #     error_rms = (np.sum((a.astype("float") - b.astype("float")) ** 2)) ** (1 / 2)
        #     error_rms = error_rms / a.size
        #
        #     error_euc = (((a - b) ** 2).sum(axis=2) ** 0.5).sum()
        #     error_euc = error_euc / a.size
        #
        #     print("a")

        return -1

    def twoByTwoAnalysis(self, problem):
        twoByTwoProblem = TwoByTwoProblems(problem)

        # TODO: This probably shouldn't be first for performance reasons, but currently needs to be to avoid false positives.
        answer = twoByTwoProblem.checkEqualImageDifference(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using checkEqualImageDifference")
            return answer

        answer = twoByTwoProblem.areABEqual(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using findDWhenABAreEqual")
            return answer

        answer = twoByTwoProblem.areACEqual(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using findDWhenACAreEqual")
            return answer

        answer = twoByTwoProblem.check_vertical_reflection(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using checkVerticalReflection")
            return answer

        answer = twoByTwoProblem.check_horizontal_reflection(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using checkHorizontalReflection")
            return answer

        answer = twoByTwoProblem.check_rotation(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using check_rotation")
            return answer

        answer = twoByTwoProblem.check_for_solid_and_outline(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using check_for_solid_and_outline")
            return answer

        # Default a guess to 1
        print(problem.name + ": 1 using default")
        return 1



    def threeByThreeAnalysis(self, problem):
        threeByThreeProblem = ThreeByThreeProblems(problem)

        answer = threeByThreeProblem.check_equal_row(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using check_equal_row")
            return answer

        answer = threeByThreeProblem.consistent_change_in_row(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using consistent_change_in_row")
            return answer






        # Default a guess to 1
        print(problem.name + ": 1 using default")
        return 1





    # TODO: Check if all images in a row are the same, if so, find the similar image for the last row






class TwoByTwoProblems:

    def __init__(self, problem):
        self.problem = problem

    # Check if A and B are equal. If so, find the answer that is equal to C.
    def areABEqual(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]

        imageA = self.convert_black_white(Image.open(figureA.visualFilename))
        imageB = self.convert_black_white(Image.open(figureB.visualFilename))
        imageC = self.convert_black_white(Image.open(figureC.visualFilename))

        if self.check_equal(imageA, imageB):
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.check_equal(imageC, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        return -1

    # Check if A and C are equal. If so, find the answer that is equal to B.
    def areACEqual(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]

        imageA = self.convert_black_white(Image.open(figureA.visualFilename))
        imageB = self.convert_black_white(Image.open(figureB.visualFilename))
        imageC = self.convert_black_white(Image.open(figureC.visualFilename))

        if self.check_equal(imageA, imageC):
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.check_equal(imageB, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        return -1

    # Check if one image is equal to another and account for slight pixel variations
    def check_equal(self, image1, image2):
        diff = ImageChops.difference(image1, image2)
        data = diff.getdata()
        if diff.getbbox() is None:
            return True
        pixelCount = 0
        blackCount = 0
        if data.mode == 'RGBA':
            for pixel in data:
                pixelCount += 1
                if pixel == (0, 0, 0, 0):
                    blackCount += 1
        elif data.mode == 'RGB':
            for pixel in data:
                pixelCount += 1
                if pixel == (0, 0, 0):
                    blackCount += 1
        elif data.mode == 'L':
            for pixel in data:
                pixelCount += 1
                if pixel == 0:
                    blackCount += 1
        if blackCount / pixelCount > 0.95:
            return True
        return False

    # Search for a vertical reflection pattern. If detected, solve for D.
    def check_vertical_reflection(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]

        rotatedImageA = self.convert_black_white(Image.open(figureA.visualFilename).transpose(Image.FLIP_LEFT_RIGHT))
        imageB = self.convert_black_white(Image.open(figureB.visualFilename))
        imageC = self.convert_black_white(Image.open(figureC.visualFilename))

        # Check if B is a vertical mirror of A. If so, find the vertical mirror of C.
        if self.check_equal(rotatedImageA, imageB):
            rotatedImageC = self.convert_black_white(imageC.transpose(Image.FLIP_LEFT_RIGHT))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.check_equal(rotatedImageC, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        # Check if C is a vertical mirror of A. If so, find the vertical mirror of B.
        if self.check_equal(rotatedImageA, imageC):
            rotatedImageB = imageB.transpose(Image.FLIP_LEFT_RIGHT)
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.check_equal(rotatedImageB, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        # If no vertical mirror found, return -1
        return -1

    # Search for a horizontal reflection pattern. If detected, solve for D.
    def check_horizontal_reflection(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]

        rotatedImageA = self.convert_black_white(Image.open(figureA.visualFilename).transpose(Image.FLIP_TOP_BOTTOM))
        imageB = self.convert_black_white(Image.open(figureB.visualFilename))
        imageC = self.convert_black_white(Image.open(figureC.visualFilename))

        # Check if B is a horizontal mirror of A. If so, find the horizontal mirror of C.
        if self.check_equal(rotatedImageA, imageB):
            rotatedImageC = imageC.transpose(Image.FLIP_TOP_BOTTOM)
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.check_equal(rotatedImageC, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        # Check if C is a horizontal mirror of A. If so, find the horizontal mirror of B.
        if self.check_equal(rotatedImageA, imageC):
            rotatedImageB = imageB.transpose(Image.FLIP_TOP_BOTTOM)
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.check_equal(rotatedImageB, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        # If no horizontal mirror found, return -1
        return -1

    # Search for a rotation match. If detected, solve for D
    def check_rotation(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]

        # Check if B is a rotation of A. If so, find the equivalent rotation of C.
        rotation = self.determine_rotation_amount(self.convert_black_white(Image.open(figureA.visualFilename)), self.convert_black_white(Image.open(figureB.visualFilename)))
        if rotation > 0:
            rotatedImageC = self.convert_black_white(Image.open(figureC.visualFilename).rotate(rotation))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.check_equal(rotatedImageC, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        # Check if C is a rotation of A. If so, find the equivalent rotation of B.
        rotation = self.determine_rotation_amount(self.convert_black_white(Image.open(figureA.visualFilename)), self.convert_black_white(Image.open(figureC.visualFilename)))
        if rotation > 0:
            rotatedImageB = self.convert_black_white(Image.open(figureC.visualFilename).rotate(rotation))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.check_equal(rotatedImageB, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        return -1

    def determine_rotation_amount(self, image1, image2):
        if self.check_equal(image1.rotate(90), image2):
            return 90
        if self.check_equal(image1.rotate(180), image2):
            return 180
        if self.check_equal(image1.rotate(270), image2):
            return 270
        return -1

    def checkEqualImageDifference(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]

        diff1 = ImageChops.difference(self.convert_black_white(Image.open(figureA.visualFilename)), self.convert_black_white(Image.open(figureB.visualFilename)))

        oldPixelRatio = 0.0
        pixelRatio = 0.0
        bestAnswer = -1
        for key in figures:
            if key.isalpha():
                continue
            figure = figures[key]
            diff2 = ImageChops.difference(self.convert_black_white(Image.open(figureC.visualFilename)), self.convert_black_white(Image.open(figure.visualFilename)))
            if self.check_equal_simple(diff1, diff2):
                return int(figure.name)

            pixelRatio = self.get_pixel_ratio(diff1, diff2)
            if pixelRatio > oldPixelRatio:
                oldPixelRatio = pixelRatio
                bestAnswer = int(figure.name)

        if oldPixelRatio >= 0.97:
            return bestAnswer

        return -1

    def check_equal_simple(self, image1, image2):
        diff = ImageChops.difference(image1, image2)
        # image1.show()
        # image2.show()
        # diff.show()
        if diff.getbbox() is None:
            return True

    def get_pixel_ratio(self, image1, image2):
        diff = ImageChops.difference(image1, image2)
        pixelCount = 0
        blackCount = 0
        data = diff.getdata()
        if data.mode == 'RGBA':
            for pixel in data:
                pixelCount += 1
                if pixel == (0, 0, 0, 0):
                    blackCount += 1
        elif data.mode == 'RGB':
            for pixel in data:
                pixelCount += 1
                if pixel == (0, 0, 0):
                    blackCount += 1
        elif data.mode == 'L':
            for pixel in data:
                pixelCount += 1
                if pixel == 0:
                    blackCount += 1
        pixelRatio = blackCount / pixelCount
        return pixelRatio

    def check_for_solid_and_outline(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]

        imageA = self.convert_black_white(Image.open(figureA.visualFilename))
        imageB = self.convert_black_white(Image.open(figureB.visualFilename))
        imageC = self.convert_black_white(Image.open(figureC.visualFilename))

        diff = ImageChops.difference(imageA, imageB)
        diff = diff.convert('L')
        invertedDiff = PIL.ImageOps.invert(diff)

        pixelRatioDiff = self.dark_pixel_ratio(invertedDiff)
        pixelRatioA = self.dark_pixel_ratio(imageA.convert('L'))
        pixelRatioB = self.dark_pixel_ratio(imageB.convert('L'))
        pixelDifferenceA = abs(pixelRatioDiff - pixelRatioA)
        pixelDifferenceB = abs(pixelRatioDiff - pixelRatioB)

        # Check which image (A or B) is less. Whichever is less, see if it is has least 0.005 pixel similarity.
        # If yes, then this is likely a solid/bordered problem and solve for D
        bestRatio = 1.0
        newRatio = 1.0
        bestAnswer = -1
        if min(pixelDifferenceA, pixelDifferenceB) <= 0.005:
            pixelRatioC = self.dark_pixel_ratio(imageC.convert('L'))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageN = self.convert_black_white(Image.open(figure.visualFilename))
                diff = ImageChops.difference(imageC, imageN)
                diff = diff.convert('L')
                invertedDiff = PIL.ImageOps.invert(diff)
                # invertedDiff.show()

                pixelRatioDiff = self.dark_pixel_ratio(invertedDiff)
                pixelRatioD = self.dark_pixel_ratio(imageN.convert('L'))
                pixelDifferenceC = abs(pixelRatioDiff - pixelRatioC)
                pixelDifferenceD = abs(pixelRatioDiff - pixelRatioD)

                # Similar to the parent if statement, if the difference is within 0.005, this is likely the answer.
                # Iterate through, until the closest similarity was found.
                newRatio = min(pixelDifferenceC, pixelDifferenceD)
                if newRatio <= 0.005 and newRatio < bestRatio:
                    bestRatio = newRatio
                    bestAnswer = int(figure.name)

        return bestAnswer

    def dark_pixel_ratio(self, image):
        pixelCount = 0
        blackCount = 0

        data = image.getdata()
        # image.show()
        if data.mode == 'RGBA':
            for pixel in data:
                pixelCount += 1
                if pixel == (0, 0, 0, 255):
                    blackCount += 1
        elif data.mode == 'RGB':
            for pixel in data:
                pixelCount += 1
                if pixel == (0, 0, 0):
                    blackCount += 1
        elif data.mode == 'L':
            for pixel in data:
                pixelCount += 1
                if pixel <= 127:
                    blackCount += 1
        pixelRatio = blackCount / pixelCount
        return pixelRatio

    def check_equal_RMS(self, image1, image2):
        arr1 = np.array(image1)
        arr2 = np.array(image2)

        error = (np.sum((arr1.astype("float") - arr2.astype("float"))**2))**(.5)
        error = error / arr1.size

        if error < 0.3:
            return True
        return False

    def convert_black_white(self, image):
        image = image.convert('L')
        pixels = image.load()
        for i in range(image.size[0]):  # for every pixel:
            for j in range(image.size[1]):
                if pixels[i, j] < 127:
                    pixels[i, j] = 0
                else:
                    pixels[i, j] = 255

        return image



class ThreeByThreeProblems:


    def __init__(self, problem):
        self.problem = problem

##############  Utility Methods  ##################################################################################################

    def open_black_white_conversion(self, figureName):
        image = self.convert_black_white(Image.open(figureName))
        return image

    def convert_black_white(self, image):
        image = image.convert('L')
        pixels = image.load()
        for i in range(image.size[0]):  # for every pixel:
            for j in range(image.size[1]):
                if pixels[i, j] < 127:
                    pixels[i, j] = 0
                else:
                    pixels[i, j] = 255

        return image

    # def check_equal_black_white_simple(self, image1, image2):
    #     diff = ImageChops.difference(image1, image2)
    #     data = diff.getdata()
    #     if diff.getbbox() is None:
    #         return True
    #     pixelCount = 0
    #     blackCount = 0
    #     if data.mode == 'L':
    #         for pixel in data:
    #             pixelCount += 1
    #             if pixel == 0:
    #                 blackCount += 1
    #     if blackCount / pixelCount > 0.97:
    #         return True
    #     return False

    def get_dark_pixel_ratio(self, image):
        pixelCount = 0
        blackCount = 0
        data = image.getdata()
        if data.mode == 'L':
            for pixel in data:
                pixelCount += 1
                if pixel <= 127:
                    blackCount += 1
        ratio = blackCount / pixelCount
        return ratio

    def get_black_white_similarity(self, image1, image2):
        diff = ImageChops.difference(image1, image2)
        data = diff.getdata()
        if diff.getbbox() is None:
            return 1.0
        # diff.show()
        pixelCount = 0
        blackCount = 0
        if data.mode == 'L':
            for pixel in data:
                pixelCount += 1
                if pixel == 0:
                    blackCount += 1
        diffRatio = blackCount / pixelCount
        return diffRatio

    def get_RMS_value(self, image1, image2):
        arr1 = np.array(image1)
        arr2 = np.array(image2)

        error_rms = (np.sum((arr1.astype("float") - arr2.astype("float")) ** 2)) ** (0.5)
        error_rms = error_rms / arr1.size
        rms_similar = 1 - error_rms

        return rms_similar

    def get_euclidean_diff(self, image1, image2):
        arr1 = np.array(image1)
        arr2 = np.array(image2)

        eucDiff = (((arr1 - arr2) ** 2).sum(axis=1) ** (1/2)).sum()
        eucDiff = eucDiff / arr1.size
        eucSimilarity = 1 - eucDiff
        return eucSimilarity

    def get_dark_pixel_similarity_ratio(self, image1, image2):

        pixelCount = 0
        blackCount = 0
        data = image1.getdata()
        if data.mode == 'L':
            for pixel in data:
                pixelCount += 1
                if pixel <= 127:
                    blackCount += 1
        ratio1 = blackCount/pixelCount

        pixelCount = 0
        blackCount = 0
        data = image2.getdata()
        if data.mode == 'L':
            for pixel in data:
                pixelCount += 1
                if pixel <= 127:
                    blackCount += 1
        ratio2 = blackCount / pixelCount

        ratioDiff = abs(ratio1 - ratio2)
        ratioSimilar = 1 - ratioDiff
        return ratioSimilar

    def robust_comparison_value(self, image1, image2):
        # diffRatio = self.get_black_white_similarity(image1, image2)
        # if diffRatio == 1.0:
        #     return diffRatio
        eucSimilarity = self.get_euclidean_diff(image1, image2)
        darkPixelRatio = self.get_dark_pixel_similarity_ratio(image1, image2)
        # rmsSimilar = self.get_RMS_value(image1, image2)

        robustValue = (eucSimilarity + darkPixelRatio) / 2
        return robustValue

##############  Solution methods  ##################################################################################################

    def check_equal_row(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]
        figureD = figures["D"]
        figureE = figures["E"]
        figureF = figures["F"]
        figureG = figures["G"]
        figureH = figures["H"]

        imageA = self.open_black_white_conversion(figureA.visualFilename)
        imageB = self.open_black_white_conversion(figureB.visualFilename)
        imageC = self.open_black_white_conversion(figureC.visualFilename)

        robustValueAB = self.robust_comparison_value(imageA, imageB)
        # robustValueBC = self.robust_comparison_value(imageB, imageC)
        robustValueAC = self.robust_comparison_value(imageA, imageC)
        # If ABC not equal, move on
        if robustValueAB < 0.995 or robustValueAC < 0.995:
            return -1

        imageD = self.open_black_white_conversion(figureD.visualFilename)
        imageE = self.open_black_white_conversion(figureE.visualFilename)
        imageF = self.open_black_white_conversion(figureF.visualFilename)

        robustValueDE = self.robust_comparison_value(imageD, imageE)
        # robustValueEF = self.robust_comparison_value(imageE, imageF)
        robustValueDF = self.robust_comparison_value(imageD, imageF)
        # If DEF not equal move on
        if robustValueDE < 0.995 or robustValueDF < 0.995:
            return -1

        imageG = self.open_black_white_conversion(figureG.visualFilename)
        imageH = self.open_black_white_conversion(figureH.visualFilename)

        robustValueGH = self.robust_comparison_value(imageG, imageH)
        potentialAnswer = -1
        if robustValueGH >= 0.995:
            bestAnswerValue = 0
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                currentAnswerValue = self.robust_comparison_value(imageG, imageAnswer)
                if currentAnswerValue > bestAnswerValue:
                    bestAnswerValue = currentAnswerValue
                    potentialAnswer = int(figure.name)

        return potentialAnswer

    def consistent_change_in_row(self, problem):
        # if the number of black pixels added/subtracted between A and B is the same as B and C, find the difference between G and H and the closest difference between H and all answers
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]
        figureD = figures["D"]
        figureE = figures["E"]
        figureF = figures["F"]
        figureG = figures["G"]
        figureH = figures["H"]

        imageA = self.open_black_white_conversion(figureA.visualFilename)
        imageB = self.open_black_white_conversion(figureB.visualFilename)
        imageC = self.open_black_white_conversion(figureC.visualFilename)
        imageD = self.open_black_white_conversion(figureD.visualFilename)
        imageE = self.open_black_white_conversion(figureE.visualFilename)
        imageF = self.open_black_white_conversion(figureF.visualFilename)
        imageG = self.open_black_white_conversion(figureG.visualFilename)
        imageH = self.open_black_white_conversion(figureH.visualFilename)


        eucSimilarityAB = self.get_euclidean_diff(imageA, imageB)
        darkPixelRatioAB = self.get_dark_pixel_similarity_ratio(imageA, imageB)
        eucSimilarityBC = self.get_euclidean_diff(imageB, imageC)
        darkPixelRatioBC = self.get_dark_pixel_similarity_ratio(imageB, imageC)
        ABCEucDiff = abs(eucSimilarityAB - eucSimilarityBC)
        ABCDarkPixelDiff = abs(darkPixelRatioAB - darkPixelRatioBC)
        if ABCDarkPixelDiff >= 0.01 or ABCEucDiff >= 0.01:
            return -1

        eucSimilarityDE = self.get_euclidean_diff(imageD, imageE)
        darkPixelRatioDE = self.get_dark_pixel_similarity_ratio(imageD, imageE)
        eucSimilarityEF = self.get_euclidean_diff(imageE, imageF)
        darkPixelRatioEF = self.get_dark_pixel_similarity_ratio(imageE, imageF)
        DEFEucDiff = abs(eucSimilarityDE - eucSimilarityEF)
        DEFDarkPixelDiff = abs(darkPixelRatioDE - darkPixelRatioEF)
        if DEFDarkPixelDiff >= 0.01 or DEFEucDiff >= 0.01:
            return -1

        eucSimilarityGH = self.get_euclidean_diff(imageG, imageH)
        darkPixelRatioGH = self.get_dark_pixel_similarity_ratio(imageG, imageH)
        GDarkPixel = self.get_dark_pixel_ratio(imageG)
        HDarkPixel = self.get_dark_pixel_ratio(imageH)


        #THEN FIND BEST, NOT FIRST
        #Count approximate added pixels
        potentialAnswer = -1
        bestEucSimilarity = 1.0
        bestDarkPixelRatio = 1.0
        for key in figures:
            if key.isalpha():
                continue
            # if key != "7" and key != "8":
            #     continue
            figure = figures[key]
            imageAnswer = self.open_black_white_conversion(figure.visualFilename)
            AnswerDarkPixel = self.get_dark_pixel_ratio(imageAnswer)

            if (GDarkPixel < HDarkPixel and HDarkPixel < AnswerDarkPixel) or (GDarkPixel > HDarkPixel and HDarkPixel > AnswerDarkPixel):
                eucSimilarityHAnswer = self.get_euclidean_diff(imageH, imageAnswer)
                darkPixelRatioHAnswer = self.get_dark_pixel_similarity_ratio(imageH, imageAnswer)
                currentAnswerEucDiff = abs(eucSimilarityGH - eucSimilarityHAnswer)
                currentDarkPixelDiff = abs(darkPixelRatioGH - darkPixelRatioHAnswer)

                if (currentDarkPixelDiff < bestDarkPixelRatio) and (currentAnswerEucDiff < bestEucSimilarity):
                    bestDarkPixelRatio = currentDarkPixelDiff
                    bestEucSimilarity = currentAnswerEucDiff
                    potentialAnswer = int(figure.name)
                elif currentDarkPixelDiff < bestDarkPixelRatio:
                    bestDarkPixelRatio = currentDarkPixelDiff
                    bestEucSimilarity = currentAnswerEucDiff
                    potentialAnswer = int(figure.name)
                # elif currentAnswerEucDiff < bestEucSimilarity:
                #     bestEucSimilarity = currentAnswerEucDiff
                #     bestDarkPixelRatio = currentDarkPixelDiff
                #     potentialAnswer = int(figure.name)

        return potentialAnswer







# IDEA FOR C7: Do something similar to the equation above, but check for reflections/rotations. Maybe account for no black pixel changes?
# IDEA FOR C9: Check if half of the image is symmetrical? OR check half of A reversed against C? Probably the second one.
# C12 is reliably passing with the consistent_change_in_row method, but it isn't passing for the right reasons. Write a new method for this kind of thing?






##############  EXPERIMENTAL methods  ##################################################################################################

    # This is just a test to see how well these new comparisons work
    def check_2x2_with_new_technique(self, problem):
        figures = problem.figures
        figureA = figures["A"]
        figureB = figures["B"]
        figureC = figures["C"]

        imageA = self.open_black_white_conversion(figureA.visualFilename).transpose(Image.FLIP_LEFT_RIGHT)
        imageB = self.open_black_white_conversion(figureB.visualFilename)

        robustValue = self.robust_comparison_value(imageA, imageB)
        print(robustValue)