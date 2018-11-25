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

        answer = threeByThreeProblem.check_corner_reflections(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using check_Corner_Reflections")
            return answer

        answer = threeByThreeProblem.reverse_image_halves_comparison(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using reverse_image_halves_comparison")
            return answer

        # Project 3 solutions
        answer = threeByThreeProblem.combine_panels(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using combine_panels")
            return answer

        answer = threeByThreeProblem.detect_row_shift(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using detect_row_shift")
            return answer













        answer = threeByThreeProblem.combine_row_column_similarities_2_factors(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using combine_row_column_similarities_2_factors")
            return answer

        # Call this method last to avoid false positives
        answer = threeByThreeProblem.combine_row_column_similarities(problem)
        if answer > 0:
            print(problem.name + ": " + str(answer) + " using combine_row_column_similarities")
            return answer

        # Default a guess to 1
        print(problem.name + ": 1 using default")
        return 1


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

        if self.robust_comparison_boolean(imageA, imageB):
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.robust_comparison_boolean(imageC, self.convert_black_white(Image.open(figure.visualFilename))):
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

        if self.robust_comparison_boolean(imageA, imageC):
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.robust_comparison_boolean(imageB, self.convert_black_white(Image.open(figure.visualFilename))):
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
        if self.robust_comparison_boolean(rotatedImageA, imageB):
            rotatedImageC = self.convert_black_white(imageC.transpose(Image.FLIP_LEFT_RIGHT))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.robust_comparison_boolean(rotatedImageC, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        # Check if C is a vertical mirror of A. If so, find the vertical mirror of B.
        if self.robust_comparison_boolean(rotatedImageA, imageC):
            rotatedImageB = imageB.transpose(Image.FLIP_LEFT_RIGHT)
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.robust_comparison_boolean(rotatedImageB, self.convert_black_white(Image.open(figure.visualFilename))):
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
        if self.robust_comparison_boolean(rotatedImageA, imageB):
            rotatedImageC = imageC.transpose(Image.FLIP_TOP_BOTTOM)
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.robust_comparison_boolean(rotatedImageC, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        # Check if C is a horizontal mirror of A. If so, find the horizontal mirror of B.
        if self.robust_comparison_boolean(rotatedImageA, imageC):
            rotatedImageB = imageB.transpose(Image.FLIP_TOP_BOTTOM)
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.robust_comparison_boolean(rotatedImageB, self.convert_black_white(Image.open(figure.visualFilename))):
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
                if self.robust_comparison_boolean(rotatedImageC, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        # Check if C is a rotation of A. If so, find the equivalent rotation of B.
        rotation = self.determine_rotation_amount(self.convert_black_white(Image.open(figureA.visualFilename)), self.convert_black_white(Image.open(figureC.visualFilename)))
        if rotation > 0:
            rotatedImageB = self.convert_black_white(Image.open(figureC.visualFilename).rotate(rotation))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                if self.robust_comparison_boolean(rotatedImageB, self.convert_black_white(Image.open(figure.visualFilename))):
                    return int(figure.name)

        return -1

    def determine_rotation_amount(self, image1, image2):
        if self.robust_comparison_boolean(image1.rotate(90), image2):
            return 90
        if self.robust_comparison_boolean(image1.rotate(180), image2):
            return 180
        if self.robust_comparison_boolean(image1.rotate(270), image2):
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
        eucSimilarity = self.get_euclidean_diff(image1, image2)
        darkPixelRatio = self.get_dark_pixel_similarity_ratio(image1, image2)

        robustValue = (eucSimilarity + darkPixelRatio) / 2
        return robustValue

    def robust_comparison_boolean(self, image1, image2):
        eucSimilarity = self.get_euclidean_diff(image1, image2)
        darkPixelRatio = self.get_dark_pixel_similarity_ratio(image1, image2)

        robustValue = (eucSimilarity + darkPixelRatio) / 2
        if robustValue >= 0.995:
            return True
        return False



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

    def robust_comparison_boolean(self, image1, image2):
        eucSimilarity = self.get_euclidean_diff(image1, image2)
        darkPixelRatio = self.get_dark_pixel_similarity_ratio(image1, image2)

        robustValue = (eucSimilarity + darkPixelRatio) / 2
        if robustValue >= 0.995:
            return True
        return False

    def reverse_image_halves(self, image):
        height, width = image.size
        widthHalf = width // 2

        # Left Half
        leftHalf = image.copy()
        leftHalf = leftHalf.crop((0, 0, widthHalf, height))

        # Right Half
        rightHalf = image.copy()
        rightHalf = rightHalf.crop((widthHalf, 0, width, height))

        # Swap sides
        newImage = Image.new('L', (width, height))
        newImage.paste(rightHalf, (0, 0))
        newImage.paste(leftHalf, (widthHalf, 0))

        return newImage

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
        if ABCDarkPixelDiff >= 0.01 or ABCEucDiff >= 0.01 or self.get_dark_pixel_similarity_ratio(imageA, imageC) >= 0.995:
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

    def check_corner_reflections(self, problem):
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
        verticalFlipA = self.convert_black_white(Image.open(figureA.visualFilename).transpose(Image.FLIP_LEFT_RIGHT))
        horizontalFlipA = self.convert_black_white(Image.open(figureA.visualFilename).transpose(Image.FLIP_TOP_BOTTOM))
        imageB = self.open_black_white_conversion(figureB.visualFilename)
        verticalFlipB = self.convert_black_white(Image.open(figureB.visualFilename).transpose(Image.FLIP_LEFT_RIGHT))
        horizontalFlipB = self.convert_black_white(Image.open(figureB.visualFilename).transpose(Image.FLIP_TOP_BOTTOM))

        imageC = self.open_black_white_conversion(figureC.visualFilename)

        imageD = self.open_black_white_conversion(figureD.visualFilename)
        verticalFlipD = self.convert_black_white(Image.open(figureD.visualFilename).transpose(Image.FLIP_LEFT_RIGHT))
        horizontalFlipD = self.convert_black_white(Image.open(figureD.visualFilename).transpose(Image.FLIP_TOP_BOTTOM))
        imageE = self.open_black_white_conversion(figureE.visualFilename)
        imageF = self.open_black_white_conversion(figureF.visualFilename)

        imageG = self.open_black_white_conversion(figureG.visualFilename)
        imageH = self.open_black_white_conversion(figureH.visualFilename)

        # AC and DF Vertical Mirror
        if self.robust_comparison_boolean(verticalFlipA, imageC) and self.robust_comparison_boolean(verticalFlipD, imageF):
            verticalFlipG = self.convert_black_white(Image.open(figureG.visualFilename).transpose(Image.FLIP_LEFT_RIGHT))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                if self.robust_comparison_boolean(verticalFlipG, imageAnswer):
                    return int(figure.name)

        # AC and DF Horizontal Mirror
        if self.robust_comparison_boolean(horizontalFlipA, imageC) and self.robust_comparison_boolean(horizontalFlipD, imageF):
            horizontalFlipG = self.convert_black_white(Image.open(figureG.visualFilename).transpose(Image.FLIP_TOP_BOTTOM))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                if self.robust_comparison_boolean(horizontalFlipG, imageAnswer):
                    return int(figure.name)

        # AG and BF Vertical Mirror
        if self.robust_comparison_boolean(verticalFlipA, imageG) and self.robust_comparison_boolean(verticalFlipB, imageH):
            verticalFlipC = self.convert_black_white(Image.open(figureC.visualFilename).transpose(Image.FLIP_LEFT_RIGHT))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                if self.robust_comparison_boolean(verticalFlipC, imageAnswer):
                    return int(figure.name)

        # AG and BF Horizontal Mirror
        if self.robust_comparison_boolean(horizontalFlipA, imageG) and self.robust_comparison_boolean(horizontalFlipB, imageH):
            horizontalFlipB = self.convert_black_white(Image.open(figureC.visualFilename).transpose(Image.FLIP_TOP_BOTTOM))
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                if self.robust_comparison_boolean(horizontalFlipB, imageAnswer):
                    return int(figure.name)

        return -1

    def reverse_image_halves_comparison(self, problem):
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

        swappedA = self.reverse_image_halves(imageA)
        swappedD = self.reverse_image_halves(imageD)
        if self.robust_comparison_value(swappedA, imageC) < 0.99 or self.robust_comparison_value(swappedD, imageF) < 0.99:
            return -1

        potentialAnswer = -1
        bestAnswerValue = 0
        for key in figures:
            if key.isalpha():
                continue
            figure = figures[key]
            swappedG = self.reverse_image_halves(imageG)
            imageAnswer = self.open_black_white_conversion(figure.visualFilename)
            comparison = self.robust_comparison_value(swappedG, imageAnswer)
            if comparison >= 0.99 and comparison > bestAnswerValue:
                bestAnswerValue = comparison
                potentialAnswer = int(figure.name)

        return potentialAnswer


# IDEA FOR C10: Check if BD, CG, FH are rotations. If so, check if C doubles A, and if F double D. If so, find double G?
    # What if B and E and H were separated already? Then they would technically have the same amount of pixels as 7.
# C12 is reliably passing with the consistent_change_in_row method, but it isn't passing for the right reasons. Write a new method for this kind of thing?


# ------------- Project 3 Methods ------------- #

    def detect_row_shift(self, problem):
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

        if self.robust_comparison_value(imageA, imageD) > 0.99 and self.robust_comparison_value(imageB, imageE) > 0.99 and self.robust_comparison_value(imageC, imageF) > 0.99:
            # compare to G/H just to be sure
            if self.robust_comparison_value(imageA, imageG) > 0.99 and self.robust_comparison_value(imageB, imageH) > 0.99:
                potentialAnswer = -1
                bestAnswerValue = 0
                for key in figures:
                    if key.isalpha():
                        continue
                    figure = figures[key]
                    imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                    comparison = self.robust_comparison_value(imageC, imageAnswer)
                    if comparison >= 0.99 and comparison > bestAnswerValue:
                        bestAnswerValue = comparison
                        potentialAnswer = int(figure.name)
                return potentialAnswer
            else:
                return -1
        elif self.robust_comparison_value(imageA, imageE) > 0.99 and self.robust_comparison_value(imageB, imageF) > 0.99 and self.robust_comparison_value(imageC, imageD) > 0.99:
            # compare to G/H just to be sure
            if self.robust_comparison_value(imageB, imageG) > 0.99 and self.robust_comparison_value(imageC, imageH) > 0.99:
                potentialAnswer = -1
                bestAnswerValue = 0
                for key in figures:
                    if key.isalpha():
                        continue
                    figure = figures[key]
                    imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                    comparison = self.robust_comparison_value(imageA, imageAnswer)
                    if comparison >= 0.99 and comparison > bestAnswerValue:
                        bestAnswerValue = comparison
                        potentialAnswer = int(figure.name)
                return potentialAnswer
            else:
                return -1
        elif self.robust_comparison_value(imageA, imageE) > 0.99 and self.robust_comparison_value(imageB, imageF) > 0.99 and self.robust_comparison_value(imageC, imageD) > 0.99:
            # compare to G/H just to be sure
            if self.robust_comparison_value(imageA, imageH) > 0.99 and self.robust_comparison_value(imageC, imageG) > 0.99:
                potentialAnswer = -1
                bestAnswerValue = 0
                for key in figures:
                    if key.isalpha():
                        continue
                    figure = figures[key]
                    imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                    comparison = self.robust_comparison_value(imageA, imageAnswer)
                    if comparison >= 0.99 and comparison > bestAnswerValue:
                        bestAnswerValue = comparison
                        potentialAnswer = int(figure.name)
                return potentialAnswer
            else:
                return -1
        else:
            return -1

    # No specialization or shifting involved
    def combine_row_column_similarities(self, problem):
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

        ABSim = ImageChops.add(imageA, imageB)
        BCSim = ImageChops.add(imageB, imageC)
        ACSim = ImageChops.add(imageA, imageC)
        # robustValue1 = self.robust_comparison_value(ABSim, ACSim)
        # robustValue2 = self.robust_comparison_value(ABSim, BCSim)
        # robustValue3 = self.robust_comparison_value(ACSim, BCSim)
        # robustAverage1 = (robustValue1 + robustValue2 + robustValue3) / 3

        ADSim = ImageChops.add(imageA, imageD)
        DGSim = ImageChops.add(imageD, imageG)
        AGSim = ImageChops.add(imageA, imageG)
        # robustValue1 = self.robust_comparison_value(ADSim, AGSim)
        # robustValue2 = self.robust_comparison_value(ADSim, DGSim)
        # robustValue3 = self.robust_comparison_value(AGSim, DGSim)
        # robustAverage2 = (robustValue1 + robustValue2 + robustValue3) / 3

        if self.robust_comparison_value(ABSim, ACSim) > 0.98 and self.robust_comparison_value(ADSim, AGSim) > 0.98:
            CFSim = ImageChops.add(imageC, imageF)
            GHSim = ImageChops.add(imageG, imageH)
            answer = ImageChops.darker(CFSim, GHSim)

            potentialAnswer = -1
            bestAnswerValue = 0
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                comparison = self.robust_comparison_value(answer, imageAnswer)
                if comparison >= 0.99 and comparison > bestAnswerValue:
                    bestAnswerValue = comparison
                    potentialAnswer = int(figure.name)
            return potentialAnswer

        return -1



    # Try a method that detects change in a shift, but only for 1 shift (since that's the only shift number I see)
    # Try to solve Basic D-04 first, as the solution to some of these will be a combination of that AND detect_row_shift

    # Some problems have two different patterns that alternate in each row. This checks for each type of pattern and tries to construct the proper combination for the answer.
    def combine_row_column_similarities_2_factors(self, problem):
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


        CDSim = ImageChops.add(imageC, imageD)
        CHSim = ImageChops.add(imageC, imageH)
        DHSim = ImageChops.add(imageD, imageH)
        robustValue1 = self.robust_comparison_value(CDSim, CHSim)
        robustValue2 = self.robust_comparison_value(CDSim, DHSim)
        robustValue3 = self.robust_comparison_value(CHSim, DHSim)
        if robustValue1 > 0.98 and robustValue2 > 0.98 and robustValue3 > 0.98:
            combo1 = ImageChops.add(CDSim, CHSim)
            CDHcombo = ImageChops.add(combo1, DHSim)
            # CDHcombo.show()
            #
            # AFSim = ImageChops.add(imageA, imageF)
            # AHSim = ImageChops.add(imageA, imageH)
            # FHSim = ImageChops.add(imageF, imageH)
            # robustValue4 = self.robust_comparison_value(AFSim, AHSim)
            # robustValue5 = self.robust_comparison_value(AFSim, FHSim)
            # robustValue6 = self.robust_comparison_value(AHSim, FHSim)
            # AFHcombo = ImageChops.add(ImageChops.add(AFSim, AHSim), FHSim)
            # AFHcombo.show()
            #
            # BFSim = ImageChops.add(imageB, imageF)
            # BGSim = ImageChops.add(imageB, imageG)
            # FGSim = ImageChops.add(imageF, imageG)
            # BFGcombo = ImageChops.add(ImageChops.add(BFSim, BGSim), FGSim)
            # BFGcombo.show()

            AESim = ImageChops.add(imageA, imageE)
            # AESim.show()
            BDSim = ImageChops.add(imageB, imageD)
            # BDSim.show()

            potentialAnswer = -1
            bestAnswerValue = 0
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageAnswer = self.open_black_white_conversion(figure.visualFilename)

                # Try to deduce pattern 1
                bestPattern1Answer = None
                bestPattern1Value = 0
                for key2 in figures:
                    if key2.isalpha():
                        continue
                    figure2 = figures[key2]
                    imageAnswer2 = self.open_black_white_conversion(figure2.visualFilename)
                    AAnswerSim = ImageChops.add(imageA, imageAnswer2)
                    EAnswerSim = ImageChops.add(imageE, imageAnswer2)
                    pattern1 = ImageChops.add(ImageChops.add(AAnswerSim, EAnswerSim), AESim)
                    # pattern1.show()

                    # Validate best pattern 1 option #############################CURRENTLY UNUSED #############################################
                    imageASubtraction = self.get_euclidean_diff(imageA, pattern1)
                    imageESubtraction = self.get_euclidean_diff(imageE, pattern1)
                    pattern1Comparison = (imageESubtraction + imageASubtraction) / 2
                    if pattern1Comparison > bestPattern1Value:
                        bestPattern1Value = pattern1Comparison
                        bestPattern1Answer = pattern1

                    # bestPattern1Answer.show()


                    # Try to deduce pattern 2
                    bestPattern2Answer = None
                    bestPattern2Value = 0
                    for key3 in figures:
                        if key3.isalpha():
                            continue
                        figure3 = figures[key3]
                        imageAnswer3 = self.open_black_white_conversion(figure3.visualFilename)
                        BAnswerSim = ImageChops.add(imageB, imageAnswer3)
                        DAnswerSim = ImageChops.add(imageD, imageAnswer3)
                        pattern2 = ImageChops.add(ImageChops.add(BAnswerSim, DAnswerSim), BDSim)
                        # pattern2.show()

                        # Validate best pattern 2 option #############################CURRENTLY UNUSED #############################################
                        imageBSubtraction = self.get_euclidean_diff(imageB, pattern2)
                        imageDSubtraction = self.get_euclidean_diff(imageD, pattern2)
                        pattern2Comparison = (imageDSubtraction + imageBSubtraction) / 2
                        if pattern2Comparison > bestPattern2Value:
                            bestPattern2Value = pattern2Comparison
                            bestPattern2Answer = pattern2
                    # bestPattern2Answer.show()


                        # Combine both patterns and attempt to match to solution
                        answer = ImageChops.darker(pattern1, pattern2)
                        # answer.show()
                        comparison = self.robust_comparison_value(answer, imageAnswer)
                        if comparison >= 0.99 and comparison > bestAnswerValue:
                            bestAnswerValue = comparison
                            potentialAnswer = int(figure.name)

                        return potentialAnswer

        return -1


    def combine_panels(self, problem):
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

        ABCombo = ImageChops.darker(imageA, imageB)
        DECombo = ImageChops.darker(imageD, imageE)

        if self.robust_comparison_value(ABCombo, imageC) > 0.99 and self.robust_comparison_value(DECombo, imageF) > 0.99:
            GHCombo = ImageChops.darker(imageG, imageH)
            for key in figures:
                if key.isalpha():
                    continue
                figure = figures[key]
                imageAnswer = self.open_black_white_conversion(figure.visualFilename)
                if self.robust_comparison_boolean(GHCombo, imageAnswer):
                    return int(figure.name)

        return -1







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