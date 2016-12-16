from django import forms

class FieldExtractionForm(forms.Form):

    query_name = forms.CharField(max_length=50, required=True)
    query_description = forms.CharField(required=True)
    query_option = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(FieldExtractionForm, self).clean()
        query_name = cleaned_data.get('query_name', '')
        query_description = cleaned_data.get('query_description', '')
        query_option = cleaned_data.get('query_option', '')
        if not query_name:
            raise forms.ValidationError("Required field")
        if not query_description:
            raise forms.ValidationError("Required field")
        return self.cleaned_data


class SavedQueryForm(forms.Form):

    query_name = forms.CharField(max_length=50, required=True)
    query_description = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(SavedQueryForm, self).clean()
        query_name = cleaned_data.get('query_name', '')
        query_description = cleaned_data.get('query_description', '')
        if not query_name:
            raise forms.ValidationError("Required field")
        if not query_description:
            raise forms.ValidationError("Required field")
        return self.cleaned_data


class GrokPatternForm(forms.Form):

    grokpattern_name = forms.CharField(max_length=50, required=True)
    grokpattern_pattern = forms.CharField(required=True)
    grokpattern_description = forms.CharField(required=True)
    enabled = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(GrokPatternForm, self).clean()
        grokpattern_name = cleaned_data.get('grokpattern_name', '')
        grokpattern_pattern = cleaned_data.get('grokpattern_pattern', '')
        grokpattern_description = cleaned_data.get('grokpattern_description', '')
        if not grokpattern_name:
            raise forms.ValidationError("Required field")
        if not grokpattern_pattern:
            raise forms.ValidationError("Required field")
        if not grokpattern_description:
            raise forms.ValidationError("Required field")
        return self.cleaned_data

# class DBQueryForm(forms.Form):
#
#     query_name = forms.CharField(max_length=100, required=True)
#     query_description = forms.CharField(required=True)
#
#     def clean(self):
#         cleaned_data = super(DBQueryForm, self).clean()
#         query_name = cleaned_data.get('query_name', '')
#         query_description = cleaned_data.get('query_description', '')
#         if not query_name:
#             raise forms.ValidationError("Required field")
#         if not query_description:
#             raise forms.ValidationError("Required field")
#         return self.cleaned_data

class ESQueryForm(forms.Form):

    query_name = forms.CharField(max_length=100, required=True)
    query_description = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(ESQueryForm, self).clean()
        query_name = cleaned_data.get('query_name', '')
        query_description = cleaned_data.get('query_description', '')
        if not query_name:
            raise forms.ValidationError("Required field")
        if not query_description:
            raise forms.ValidationError("Required field")
        return self.cleaned_data