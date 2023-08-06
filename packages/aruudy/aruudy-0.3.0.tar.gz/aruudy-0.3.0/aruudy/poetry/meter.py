#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ar_metre.py
#  processing and detecting the metre of arabic poetery
#
#  Copyright 2019 Abdelkrime Aries <kariminfo0@gmail.com>
#
#  ---- AUTHORS ----
#  2019  Abdelkrime Aries <kariminfo0@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
from aruudy.poetry import bahr

# sun letters in arabic
SUN = u"([تثدذرزسشصضطظلن])"
# alif in the middle of sentence
# DORJ = spaces or (bi-, li-)kasra? or (ka-, fa-, wa-)fatha?
DORJ = u"([^\\s]\\s+|[\u0644\u0628][\u0650]?|[\u0643\u0641\u0648][\u064E]?)"

# ahruf al3illa: alif, alif maqsura, waw, yaa
ILLA = u"[اىوي]"


def normalize(text):
    res = text #result

    # Filtering
    # ===========
    #delete tatweel
    res = re.sub(u"\u0640", u"", res)

    #delete any non wanted char
    res = re.sub(u"[^\u0621-\u0652\\s]", u"", res)

    # Tashkiil
    # ===========

    # allati التِي
    res = res = re.sub(u"(^|\\s)\u0627\u0644\u0651?\u064E?\u062A\u0650\u064A(\\s|$)", u"\\1\u0627\u0644\u0651\u064E\u062A\u0650\u064A\\2", res)

    # if fatha damma or kasra is before shadda: switch
    res = res = re.sub(u"([\u064B-\u0650])\u0651", u"\u0651\\1", res)

    # add Fatha to first al-
    res = re.sub(u"^\\s*\u0627\u0644", u"\u0627\u064E\u0644", res)

    # Falty fathatan on alif fix
    res = re.sub(u"([^\\s])\u064E?([\u0627\u0649])\u064B", u"\\1\u064B\\2", res)

    # add Fatha to any non diacretized char preceeding alif
    res = re.sub(u"([^\u064B-\u0651\\s])(\u0627|\u0649)([^\u064E\u064F\u0650\u0652])", u"\\1\u064E\\2\\3", res)

    # if alif is preceeding waw: add sukuun to alif
    res = re.sub(u"\u0627\u0648", u"\u0627\u0652\u0648", res)

    #add Damma to any non diacretized char preceeding waw
    res = re.sub(u"([^\u064E\u064F\u0650\u0652\\s])\u0648([^\u064E\u064F\u0650\u0652])", u"\\1\u064F\u0648\\2", res)

    #add Kasra to any non diacretized char preceeding yaa
    res = re.sub(u"([^\u064E\u064F\u0650\u0652\\s])\u064A([^\u064E\u064F\u0650\u0652]|$)", u"\\1\u0650\u064A\\2", res)

    # add Shadda to shamsi characters after al-
    res = re.sub(u"(^|\\s)\u0627\u0644" + SUN + u"([^\u0651])", u"\\1\u0627\u0644\\2\u0651\\3", res)

    # add madda to other characters after al-
    res = re.sub(u"((?:^|\\s)\u0627\u0644[^\u0651])([^\u064E-\u0651])", u"\\1\u0653\\2", res)

    # add kasra to li
    res = re.sub(u"(^|\\s)\u0644([^\u064E-\u0652])", u"\\1\u0644\u0650\\2", res)

    # add kasra to bi
    res = re.sub(u"(^|\\s)\u0628([^\u064E-\u0652])", u"\\1\u0628\u0650\\2", res)

    # add fatha to fa
    res = re.sub(u"(^|\\s)\u0641([^\u064E-\u0652])", u"\\1\u0641\u064E\\2", res)

    # add fatha to wa
    res = re.sub(u"(^|\\s)\u0648([^\u064E-\u0652])", u"\\1\u0648\u064E\\2", res)

    # madda over alif with no fatha or damma
    res = re.sub(u"\u0623([^\u064E\u064F])", u"\u0623\u0653\\1", res)

    # hamza under alif with no kasra
    res = re.sub(u"\u0625([^\u0650])", u"\u0625\u0650\\1", res)

    #shadda not followed by a diacritic: add a madda above
    res = res = re.sub(u"\u0651([^\u064B-\u0650])", u"\u0651\u0653\\1", res)

    #add madda to any leading letter except alif
    res = res = re.sub(u"(^|\\s)([^\u0627])([^\u064E-\u0652])", u"\\1\\2\u0653\\3", res)

    #after sukuun must be a haraka
    res = res = re.sub(u"\u0652([^\\s])([^\u064B-\u0650\\s])", u"\u0652\\1\u0653\\2", res)

    return res

# https://ar.wikipedia.org/wiki/عروض

def _prosody_del(text):
    res = text

    # Replace al- with sun character (it can be preceded by prepositions bi- li-)
    # والصِّدق، والشَّمس ---> وصصِدق، وَششَمس
    res = re.sub(DORJ + u"\u0627\u0644" + SUN , u"\\1\\2", res)

    # Replace al- with l otherwise
    # # والكتاب، فالعلم ---> وَلكتاب، فَلعِلم
    res = re.sub(DORJ + u"\u0627\u0644", u"\\1\u0644", res)


    # delete first alif of a word in the middle of sentence
    # فاستمعَ، وافهم، واستماعٌ، وابنٌ، واثنان ---> فَستَمَعَ، وَفهَم، وَستِماعُن، وَبنُن، وَثنانِ
    res = re.sub(DORJ + u"\u0627([^\\s][^\u064B-\u0651\u0653])" , u"\\1\\2", res)

    # delete ending alif, waw and yaa preceeding a sakin
    # أتى المظلوم إلى القاضي فأنصفه قاضي العدل ---> أتَ لمظلوم إلَ لقاضي فأنصفه قاضِ لعدل.
    res = re.sub(ILLA + u"\\s+(.[^\u064B-\u0651\u0653])", u" \\1", res)

    # delete alif of plural masculin conjugation
    # رجعوا ---> رجعو
    res = re.sub(u"[\u064F]?\u0648\u0627(\\s+|$)", u"\u064F\u0648\u0652\\1", res)

    #TODO amruu
    # تحذف واو (عمرو) في الرفع والجر، مثل : حضر عَمرٌو، ذهبت إلى عَمرٍو، تكتب عروضيا هكذا : حضر عَمرُن، ذهبث إلى عَمرِن

    #تحذف الألف، والواو الزائدتين من : مائة، أنا، أولو، أولات، أولئك

    #تحذف الألف الأخيرة من الأدوات والحروف والأسماء الآتية إذا وليها ساكن : إذا، لماذا، هذا، كذا، إلا، ما، إذما، حاشا، خلا، عدا، كلا، لما

    return res


def _prosody_add(text):
    res = text

    #replace tanwiin taa marbuta by taa maftuuha
    res = re.sub(u"\u0629([\u064B-\u064D])", u"\u062A\\1", res)

    # delete alif from: fathatan + alif
    res = re.sub(u"\u064B(\u0627|\u0649)", u"\u064B", res)

    # Replace fathatan with fatha + nuun + sukuun
    res = re.sub(u"\u064B", u"\u064E\u0646\u0652", res)

    # Replace dammatun with damma + nuun + sukuun
    res = re.sub(u"\u064C", u"\u064F\u0646\u0652", res)

    # Replace kasratin with kasra + nuun + sukuun
    res = re.sub(u"\u064D", u"\u0650\u0646\u0652", res)

    # letter + Shadda ---> letter + sukuun + letter
    res = re.sub(u"(.)\u0651", u"\\1\u0652\\1", res)

    # hamza mamduuda --> alif-hamza + fatha + alif + sukuun
    res = re.sub(u"\u0622", u"\u0623\u064E\u0627\u0652", res)


    return res

#TODO trait these
"""
زيادة حرف الواو في بعض الأسماء، مثل : (طاوس، دَاود)، تكتب عروضيا هكذا : دَأوُود، طَأوُوس.
زيادة الألف في المواضع الآتية :
في بعض أسماء الإشارة، مثل : (هذا، هذه، هذان، هذين، ذلك، ذلكما، ذلكم)، تكتب عروضيا هكذا :هاذا، هاذه، هاذان، هاذين، ذالك، ذالكما، ذالكم....
في لفظ الجلالة (الله، الرحمن، إله)، تكتب عروضيا هكذا : اللاه، اَررحمان، إلاه.
في (لكن) المخففة، والمشددة (لكنَّ)، تكتب عروضيا هكذا : لكن، لاكننَ.
في لفظ (طه)، تكتب عروضيا هكذا : طاها.
أولئك، تكتب عروضيا هكذا : ألائك.
إشباع حركة حرف الروي بحيث ينشأ عن الإشباع حرفُ مدٍّ مجانسٌ لحركة حرف الروي، مثل أن يكون آخر الشطر (الحكمُ، كتابا، القمرِ)، تكتب عروضيا هكذا : الحكمو، كتابا، القَمَرِي).
تشبع حركة هاء الضمير الغائب للمفرد المذكر، وميم الجمع إن لم يترتب على ذلك كسر البيت الشعري، أو التقاء ساكنين، مثل : لهُ، بهِ، لكمُ، بكمُ، تكتب عروضيا هكذا : لهُو، بهِي، لكمُو، بكُمُو.
كاف المخاطب أو المخاطبة، ونون الرفع في الفعل المضارع، ونون جمع المذكر السالم، وتاء ضمير التكلم أو المخاطب للمذكر أو المؤنث تشبع حركتها إذا وقعت إحداها نهاية أحد الشطرين، مثل : كلامكَ، كلامُكِ، يسمعانِ، يسمعونَ، تسمعينَ، مسلمونَ، مسلمينَ، قُمتَ، قمتُ، قمتِ، تكتب عروضيا هكذا : كلامكَا، كلامكِي، يسمعانِي، يسمعونَا، تسمعينَا، مسلمونَا، مسلمينَا،، قُمتَا، قمتُو، قمتِي.
الهمزة الممدودة تكتب همزة مفتوحة بعدها ألف، مثل، آمن، قرآن، تكتب عروضيا هكذا: أَامَنَ، قرأَان.
الأحرف التي تحذف
"""


def prosody_form(text):
    res = text
    res = _prosody_del(text)
    res = _prosody_add(res)
    return res


def get_ameter (text):
    res = text

    #Delete sukuun
    res = re.sub(u"\u0652", "", res)

    #Replace fatha, damma, kasra & madda with (V) for vowel
    res = re.sub(u"[^v\\s][\u064E\u064F\u0650\u0653]", "v", res)

    #Delete spaces
    res = re.sub(u"\\s+", u"", res)

    #Replace all what is left as it was a consonent
    res = re.sub(u"[^v\\s]+", "c", res)

    # add sukuun in the end
    res = re.sub(u"v$", "vc", res)

    return res

def get_emeter (ameter):
    res = ameter
    res = res.replace("vc", "-")
    res = res.replace("v", "u")
    return res

class Shatr(object):
    def __init__(self, text):
        self.orig = text
        self.norm = normalize(text)
        self.prosody = prosody_form(self.norm)
        self.ameter = get_ameter(self.prosody)
        self.emeter = get_emeter(self.ameter)
        self.bahr = bahr.search_bahr(self.emeter, self.ameter)

    def to_dict(self, bahr=False):
        res = {
            "text": self.orig,
            "norm": self.norm,
            "prosody": self.prosody,
            "ameter": self.ameter,
            "emeter": self.emeter,
            "bahr": self.bahr
        }
        if bahr:
            if self.bahr:
                res["bahr"] = self.bahr.get_names()
            else:
                res["bahr"] = "None"
        return res


class Bayt(object):
    def __init__(self, text, sep="\t"):
        self.original = text

def process_shatr(text):
    return Shatr(text)
