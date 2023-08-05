from math import floor

from எண்ணிக்கை.நீட்டிப்புகள் import _உரை
from ..மூலம் import நீட்டிப்பு_வார்ப்புரு

தகவல்கள் = [
    '𝋠', '𝋡', '𝋢', '𝋣', '𝋤', '𝋥', '𝋦', '𝋧', '𝋨', '𝋩', '𝋪', '𝋫', '𝋬', '𝋭', '𝋮', '𝋯', '𝋰', '𝋱', '𝋲', '𝋳'
]
அக_தகவல்கள் = {அ: எ for எ, அ in enumerate(தகவல்கள்)}


class மாயாப்(நீட்டிப்பு_வார்ப்புரு):

    def எண்ணுக்கு(தன், உரை, மொழி="mayab'"):
        எண் = 0
        எதிர் = உரை.startswith('-')
        if எதிர்:
            உரை = உரை[1:]
        try:
            முழு, தசம = உரை.split('.')
        except ValueError:
            முழு = உரை
            தசம = None

        if not all(அ in அக_தகவல்கள் for அ in முழு):
            raise ValueError
        if தசம is not None and not all(அ in அக_தகவல்கள் for அ in தசம):
            raise ValueError

        for அ in முழு:
            எண் *= 20
            எண் += அக_தகவல்கள்[அ]

        if தசம is not None:
            த = 20
            for எ, அ in enumerate(தசம):
                எ_சுற்று = len(_உரை(1 / த))
                எண் += அக_தகவல்கள்[அ]/த
                எண் = round(எண், எ_சுற்று)
                த *= 20
        if எதிர்:
            எண் *= -1

        if '.' in உரை:
            return float(எண்)
        else:
            return int(எண்)

    def உரைக்கு(தன், எண், மொழி="mayab'", மொழி_மூலம்=None, தளம்=None):
        import math
        if எண் == 0:
            return தகவல்கள்[0]
        எதிர் = எண் < 0
        எண் = abs(எண்)
        try:
            தசம = float('0.' + _உரை(எண்).split('.')[1])
            முழு = floor(எண்)
        except IndexError:
            தசம = None
            முழு = எண்
        if முழு == 0:
            த_எ = 0
        else:
            த_எ = math.floor(math.log(முழு, 20)) + 1
        உரை = [தகவல்கள்[0]] * த_எ
        for எ in range(த_எ):
            த = த_எ - எ - 1
            ம = int(முழு / (20 ** த))
            உரை[எ] = தகவல்கள்[ம]
            முழு -= ம * 20**த
        உரை = ''.join(உரை)

        if தசம is not None:
            உரை += '.'
            while தசம != 0:
                எ_சுற்று = len(_உரை(தசம))
                தசம *= 20
                உரை+= தகவல்கள்[int(தசம)]
                தசம -= int(தசம)
                தசம = round(தசம, எ_சுற்று)
        if எதிர்:
            உரை = '-' + உரை
        return உரை

    def மொழிகள்(தன்):
        return ["mayab'"]

    def வழவெளி(தன், மொழி=None):
        எண்கள் = ''.join(['\\U%08x' % ord(அ) for அ in தகவல்கள்])

        வழவெளி = f'\-?(([{எண்கள்}]+([\.][{எண்கள்}]*)?)|([\.][{எண்கள்}]+))'

        return வழவெளி

