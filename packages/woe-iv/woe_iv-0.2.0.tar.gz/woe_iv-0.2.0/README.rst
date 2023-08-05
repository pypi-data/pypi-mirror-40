======
woe_iv
======






caculate woe(weight of evidence) of each feature and then iv(information value).



Features
--------

* 1 Calculation of WOE  and IV

    def WOE(cls, data, varList, type0='Con', target_id='y', resfile='result.xlsx'):
        """
        对分类变量直接进行分组统计并进行WOE、IV值 计算
        对连续型变量进行分组（default:10）后进行WOE、IV值 计算
        :param data: pandas DataFrame, mostly refer to ABT(Analysis Basics Table)
        :param varList: variable list
        :param type0: Continuous or Discontinuous(Category), 'con' is the required input for Continuous
        :param target_id: y flag when gen the train data
        :param resfile: download path of the result file of WOE and IV
        :return: pandas DataFrame, result of woe and iv value according y flag
        """
        pass

* 2 Apply of WOE repalcement of ABT

    def applyWOE(cls, X_data, X_map, var_list, id_cols_list=None, flag_y=None):
        """
        将最优分箱的结果WOE值对原始数据进行编码
        :param X_data: pandas DataFrame, mostly refer to ABT(Analysis Basics Table)
        :param X_map: pandas dataframe, map table, result of applying WOE, refer the func woe_iv.WOE
        :param var_list: variable list
        :param id_cols_list: some other features not been analysed but wanted like id, adress, etc.
        :param flag_y: y flag when gen the train data
        :return: pandas DataFrame, result of bining with y flag
        """
        pass
        
Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
