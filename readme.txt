AES

    prove that even considering the relations of middle three-round keys, there still exists no 5-round 1 input 
	active word and 1 output active word impossible differentials for AES-128.
	(record_file_i_j.txt: possible 2-polygons for our proof from the position (i/4 row, i % 4 col) to the position (j/4 row, j % 4 col))
    

Gift64

    Gift64_main_2way_compare.py
	Gift64_model.py 
	Gift64_model_diff.py
	    get the 6-round impossible differentials which cannot be detected by Sun’s method or Sasaki’s method.
		
	Gift64_main_2way_prove.py
	Gift64_model.py
	    prove that, in the search space where the input difference only actives one S-box in the first substitution and the output difference only 
		actives one S-box in the last substitution, there exists no 7-round impossible differentials for GIFT64 even taking account in the details
		of the key schedule.
	
	Gift64_main_3way.py
	Gift64_model.py
	    get d-impossible 3-polytopic transitions.
		
		
Midori

    prove that, in the search space where the input difference only actives one S-box in the first substitution and the output difference only 
	actives one S-box in the last substitution, there exists no 6-round impossible differentials for Midori64 even taking account in the details
	of the key schedule.

		 
MISTY1

    New Impossible Differentials
   
        MISTY1_max_round.py
        MISTY1_model
            search 4-round i-impossible differentials by exploiting the differential property of S-boxes.

        MISTY1_main_arbitrarity_sbox.py
        MISTY1_model_arbitrarily_sbox.py
            implement the arbitrary S-box mode of Sasaki’s method		
			
	Prove bound
		prove that there exists no 1 input active bit and 1 output active bit impossible differentials for
		5-round MISTY1 with the FL layers placed at the even rounds.
		


Present

    Present_main_2way.py
    Present_model.py
	    prove that, in the search space where the input difference only actives one S-box in the first substitution and the output difference only 
	    actives one S-box in the last substitution, there exists no 7-round impossible differentials for Present even taking account in the details
	    of the key schedule.
	
	Present_main_4way_i.py
	Present_model_i.py
	    search i-impossible 4-polytopic transitions.


PrintCipher

    PrintCipher48
	    
		PrintCipher48_main.py
		PrintCipher48_main_max_round.py
		PrintCipher48_model.py
		    prove that, in the search space where the input difference only actives one S-box in the first substitution and the output difference only 
	        actives one S-box in the last substitution, there exists no 5-round impossible differentials for PrintCipher48 even taking account in the details
	        of the key schedule.
			search all the 4-round impossible differentials for PRINTcipher48.
		
		PrintCipher48_main_3way.py
		PrintCipher48_main_3way_max_round.py
		PrintCipher48_model_3way.py
		    search impossible 3-polytopic transitions for PRINTcipher48  by considering all the details of the key schedule.
		
		PrintCipher48_main_3way_max_round_i.py
		PrintCipher48_model_3way_i.py
		    investigate the impact of the restraints of the xor keys.
			
		PrintCipher48_main_3way_max_round_ii.py
		PrintCipher48_model_3way_ii.py
		    investigate the impact of the restraints of the control keys.
			
		PrintCipher48_main_4way.py
		PrintCipher48_model_4way.py
		    search impossible 4-polytopic transitions for PRINTcipher48 by considering all the details of the key schedule.
	
	PrintCipher96
	
	    PrintCipher96_main.py
		PrintCipher96_main_max_round.py
		PrintCipher96_model.py
		    prove that, in the search space where the input difference only actives one S-box in the first substitution and the output difference only 
	        actives one S-box in the last substitution, there exists no 6-round impossible differentials for PrintCipher96 even taking account in the details
	        of the key schedule.
			search all the 5-round impossible differentials for PRINTcipher48.
			
		PrintCipher96_main_3way_1.py
		PrintCipher96_model_3way.py
		    search impossible 3-polytopic transitions for PRINTcipher96 by considering all the details of the key schedule.   


        PrintCipher96_main_4way.py
        PrintCipher96_model_4way.py
            search impossible 4-polytopic transitions for PRINTcipher96 by considering all the details of the key schedule. 
			

rc5

    rc5_v32
	
	    rc5_main32_2way.py
		rc5_main32_2way_max_round.py
		rc5_model32.py
		    search impossible differentials for rc5-32.
			
		rc5_main32_3way.py
		rc5_main32_3way_max_round.py
		rc5_model32.py
		    search impossible 3-polytopic transitions for rc5-32.
			
	rc5_v64

        rc5_main64_2way.py
		rc5_main64_2way_max_round.py
		rc5_model64.py
		    search impossible differentials for rc5-64.
			
		rc5_main64_3way.py
		rc5_main64_3way_max_round.py
		rc5_model64.py
		    search impossible 3-polytopic transitions for rc5-64.
			
			
	rc5_v128
	
	    rc5_main128_2way.py
		rc5_main128_2way_max_round.py
		rc5_model128.py
		    search impossible differentials for rc5-128.