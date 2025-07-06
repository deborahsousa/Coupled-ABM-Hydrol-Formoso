/**
* Name: FRBModel 
* Authors: Déborah S. Sousa, Cássio G. C. Coelho, Conceição de M. A. Alves, Célia G. Ralha.
* Tags: irrigation; water regulation
* The 'cycle > 1' conditions ensure that the simulation starts in the correct day (1st May)
*/
model UrubuRiverModel

global {
	//INPUTS
	//Files: matrices and shapefiles
	file shapefile_pumps <- file("../includes/bombasGAN2022.shp"); //irrigation pumps from GAN
	matrix farmers_data <- file("../includes/formoso_farmers.csv"); //Farmer agents information
	list<string> daily_date <- file("../includes/daily_date.txt");
	matrix<float> prob_CI <- file("../includes/CI-prob.csv");
	matrix<float> prob_NC <- file("../includes/NC-prob.csv");
	matrix<float> prob_CP <- file("../includes/CP-prob.csv");
	matrix<float> limits_withdrawal <- file("../includes/limits-withdrawal.csv");
	matrix level_series <- file("../includes/serie_niveis_referencias.csv");
	
	//Biennium Plan rules
	date attention_date <- date("2020-07-01");
	date restriction_date <- date("2020-08-01");
	date my_day <- starting_date update: update_my_date();
		
	//counters and time steps (dry season)
	date starting_date <- date("2020-05-01");
	float step <- 1 #day;
	int nb_days <- 123; //day count from the first to the last day of one dry season simulation
	string crop_season <- "soybean" among: ["soybean","rice"];
	int twoweeks_count update:update_twoweeks_count();	
	int day_in_twoweeks  update: update_day_in_twoweeks();

	action update_my_date type: date { //adjusts the date to save it correctly in the output file
		if cycle > 0 {
			date my_new_date <- daily_date[cycle]; 
			return my_new_date;
		} else {
			return starting_date;
		} 
	}

	action update_day_in_twoweeks type: int {
		if mod(cycle,15) != 0 or (cycle) >= 120 {
			return day_in_twoweeks + 1;
		} else {
			return 0;
		} 
	}
	
	action update_twoweeks_count type: int {
		if cycle = 0{
			return 0;
		}else if ((cycle) < 120) {
			return floor((cycle)/15);
		}else if ((cycle) >= 120) {
			return 7;
		}
	}
			
	//SCENARIOS
	//string scenario;
	//string scenario <- "S0"; //baseline + average level
	//string scenario <- "S1" ;//all CP with bdi and average level
	//string scenario <- "S1-min";//all CP with bdi and min level
	//string scenario <- "S1-max";//all CP with bdi and max level
	//string scenario <- "S2"; //all CI with bdi and average level
	//string scenario <- "S2-min";//all CI with bdi and min level
	//string scenario <- "S2-max";//all CI with bdi and max level
	//string scenario <- "S3";//all NC with bdi and average level
	//string scenario <- "S3-min";//all NC with bdi and min level
	
	//COLLECTIVE VARIABLES IN OUTPUT	
	list<float> all_pumps_daily_withdrawal update: Pump collect (each.daily_withdrawal);
	list<string> labels update: Pump collect (each.rotulo);
	
/***********
initial state****************/
	init {
		//loading parameters for scenarios simulation
		/**create Land from: shapefile_land;
		create Channel from: shapefile_channels;
		create Hidro from: shapefile_hidro;*/
		
		//creating the Pump agent
		create Pump from: shapefile_pumps;
		list<int> farmer_id_list <- Pump collect each.f_id;
		list<int> farmer_id_list <- remove_duplicates(Pump collect each.f_id);
		//save [farmer_id_list] to: "../results/Formoso/farmer_id_list.csv"  type:csv rewrite:false;
		//remove from:farmer_id_list index:53;
		//save [farmer_id_list] to: "../results/Formoso/farmer_id_list.csv"  type:csv rewrite:false;
		list<int> pump_id_list <- Pump collect each.F8;
		//save [pump_id_list] to: "../results/Formoso/pump_id_list.csv"  type:csv rewrite:false;
		//remove from:pump_id_list index:105;
		//save [pump_id_list] to: "../results/Formoso/pump_id_list.csv"  type:csv rewrite:false;
		
		//creating the Farmer agent
		create Farmer number: length(farmer_id_list);
		int i <- 0;
		loop farmer over: Farmer {
			farmer.f_id <- farmer_id_list[i];
			i <- i + 1;
		}
		
		//creating the sub-basin agent
		//create Sub_basin;		
		
		//creating the Regulator agent
		//create Regulator;

		//relate farmers to profiles, demand group and area
		loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
			loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
				int my_farmer_data_id <- int(farmers_data[0,i]);
				if Farmer[j].f_id = my_farmer_data_id{
					Farmer[j].nb_pumps <- length(Farmer[j].owned_pumps); // number of owned pumps
					Farmer[j].sub_basin <- farmers_data[3,i];	
				}
			}
		}	
		
		//Scenarios settings
		switch scenario {
			match 'S0'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].f_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}
			}		

			match 'S1'{ 
				loop farmer over:Farmer {
					farmer.profile <- 'CP';

				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CP';
				} 
			}
			
			match 'S1-min'{
				loop farmer over:Farmer {
					farmer.profile <- 'CP';
					if farmer.sub_basin = 'Urubu'{
						farmer.col_level <- 3;
					}else if farmer.sub_basin = 'DIRF'{
						farmer.col_level <- 6;
					}else if farmer.sub_basin = 'Duere'{
						farmer.col_level <- 12;
					}else if farmer.sub_basin = 'Xavante'{
						farmer.col_level <- 15;
					}else if farmer.sub_basin = 'Formoso'{
						farmer.col_level <- 9;
					}
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CP';
				} 
			}
			
			match 'S1-max'{
				loop farmer over:Farmer {
					farmer.profile <- 'CP';
					if farmer.sub_basin = 'Urubu'{
						farmer.col_level <- 2;
					}else if farmer.sub_basin = 'DIRF'{
						farmer.col_level <- 5;
					}else if farmer.sub_basin = 'Duere'{
						farmer.col_level <- 11;
					}else if farmer.sub_basin = 'Xavante'{
						farmer.col_level <- 14;
					}else if farmer.sub_basin = 'Formoso'{
						farmer.col_level <- 8;
					}
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CP';
				} 
			}	
			
			match 'S2'{
				loop farmer over:Farmer {
					farmer.profile <- 'CI';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CI';
				} 
			}
			
			match 'S2-min'{
				loop farmer over:Farmer {
					farmer.profile <- 'CI';
					if farmer.sub_basin = 'Urubu'{
						farmer.col_level <- 3;
					}else if farmer.sub_basin = 'DIRF'{
						farmer.col_level <- 6;
					}else if farmer.sub_basin = 'Duere'{
						farmer.col_level <- 12;
					}else if farmer.sub_basin = 'Xavante'{
						farmer.col_level <- 15;
					}else if farmer.sub_basin = 'Formoso'{
						farmer.col_level <- 9;
					}
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CI';
				} 
			}
			
			match 'S2-max'{
				loop farmer over:Farmer {
					farmer.profile <- 'CI';
					if farmer.sub_basin = 'Urubu'{
						farmer.col_level <- 2;
					}else if farmer.sub_basin = 'DIRF'{
						farmer.col_level <- 5;
					}else if farmer.sub_basin = 'Duere'{
						farmer.col_level <- 11;
					}else if farmer.sub_basin = 'Xavante'{
						farmer.col_level <- 14;
					}else if farmer.sub_basin = 'Formoso'{
						farmer.col_level <- 8;
					}
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CI';
				} 
			}	
			
			match 'S3'{
				loop farmer over:Farmer {
					farmer.profile <- 'NC';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'NC';
				} 
			}
			
			match 'S3-min'{
				loop farmer over:Farmer {
					farmer.profile <- 'NC';
					if farmer.sub_basin = 'Urubu'{
						farmer.col_level <- 3;
					}else if farmer.sub_basin = 'DIRF'{
						farmer.col_level <- 6;
					}else if farmer.sub_basin = 'Duere'{
						farmer.col_level <- 12;
					}else if farmer.sub_basin = 'Xavante'{
						farmer.col_level <- 15;
					}else if farmer.sub_basin = 'Formoso'{
						farmer.col_level <- 9;
					}
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'NC';
				} 
			}
			
			match 'S3-max'{
				loop farmer over:Farmer {
					farmer.profile <- 'NC';
					if farmer.sub_basin = 'Urubu'{
						farmer.col_level <- 2;
					}else if farmer.sub_basin = 'DIRF'{
						farmer.col_level <- 5;
					}else if farmer.sub_basin = 'Duere'{
						farmer.col_level <- 11;
					}else if farmer.sub_basin = 'Xavante'{
						farmer.col_level <- 14;
					}else if farmer.sub_basin = 'Formoso'{
						farmer.col_level <- 8;
					}
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'NC';
				} 
			}							
		}
		
		//relate pumps to farmers 
		loop i from: 0 to: length(pump_id_list) - 1 step: 1 {
			loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
				if Pump[i].f_id = Farmer[j].f_id {
					add Pump[i] to: Farmer[j].owned_pumps;
					Pump[i].pump_owner <- Farmer[j];
					Pump[i].f_profile <- Pump[i].pump_owner.profile;
				}
			}
		}
		
		//assign farmers' rules according to sub-basin
		ask Farmer {
			if sub_basin = 'Urubu'{
				 //col_level <- 1;//baseline
				 col_level <- 3;//dry
				 yellow_level <- 398;
				 red_level <- 220;
			}else if sub_basin = 'DIRF'{
				 col_level <- 4;
				 yellow_level <- 220;
				 red_level <- 163;
			}else if sub_basin = 'Formoso'{
				 col_level <- 7;
				 yellow_level <- 124;
				 red_level <- 87;
			}else if sub_basin = 'Duere'{
				 col_level <- 10;
				 yellow_level <- 200;
				 red_level <-140;
			}else if sub_basin = 'Xavante'{
				 col_level <- 13;
				 yellow_level <- 230;
				 red_level <- 160;
			}
		}
		
		// assign pump' probability matrix according to profile
		ask Pump {
			if f_profile = 'CP'{
				prob_matrix <- prob_CP;
			}else if f_profile = 'NC'{
				prob_matrix <- prob_NC;
			}else if f_profile = 'CI'{
				prob_matrix <- prob_CI;
			}
		}
		
		//save [Farmer collect (each.owned_pumps)] to: "../results/Formoso/farmers.csv"  type:csv rewrite:false;

		//save [Pump collect (each.pump_owner)] to: "../results/Formoso/pumps.csv"  type:csv rewrite:false;					
	}/******END INIT*****/		
			
	reflex save_daily_data when: cycle > 0{	
		save [cycle,int(self),my_day,all_pumps_daily_withdrawal] to: "../results/Formoso/scenarios-bdi/daily_withdrawal"+scenario+".csv"  type:csv rewrite:false header:false;				 
		save [labels] to: "../results/Formoso/labels.csv"  type:csv rewrite:false header:false;				 
		//string day_of_the_year <- daily_date[cycle-1];
		//write 'ciclo '+cycle+' '+day_of_the_year+' '+' '+all_pumps_daily_withdrawal;
		//list<float> all_pumps_daily_withdrawal <- Pump collect (each.daily_withdrawal);	
		//save [cycle,int(self),day_of_the_year,all_pumps_daily_withdrawal]to: "../results/exemplo1.csv"  type:csv rewrite:false header:false;				
		//save [cycle,int(self),day_of_the_year,f_daily_withdrawal]to: "../results/daily_withdrawal-farmer-100.csv"  type:csv rewrite:false;
		//save [cycle,int(self),day_of_the_year,all_pumps_daily_withdrawal]to: "../results/daily_withdrawal-pumps-1000-keepseed"+scenario+"-init0.csv"  type:csv rewrite:false;
	}
	
	reflex end_simulation when:cycle=nb_days+1{
		do pause;
	}
}/******END GLOBAL*****/

//species Sub_basin {
//	float current_level <- 500 update:level_series[col_level,cycle];//level variation at the reference gauging station [cm] //might be given as an input of a hydrological model output	
//}

species Pump {
	Pump pump;
	int F8;
	// FID;// pump identification number
	//int p_id <- FID; // pump identification number
	string rotulo; // pump identification. Source: GAN (2022).
	int nro_agente; //farmer owner identification number
	int f_id <- nro_agente; //farmer owner identification number
	matrix prob_matrix;
	list<float> p_list;
	Farmer pump_owner; //pump owner/farmer agent identification number
	string f_profile;// <- pump_owner.profile; //behaviour group of the pump's owner (cooperative profile)
	float irrigation_area; // irrigation area of the land property. Source: GAN (2022).
	int size <- 150;
	rgb color <- #black;
	float daily_withdrawal update:update_withdrawal(cycle);

	aspect default {
		draw circle(size) color:color border: #black;
	}
	
	action update_withdrawal (int cycle){
		list<float> p_list <- column_at(prob_matrix,twoweeks_count);
		int interval_index <- rnd_choice(p_list);
		float a <- limits_withdrawal[0,interval_index];
		float b <- limits_withdrawal[1,interval_index];
		daily_withdrawal <- rnd(a,b);
		ask pump_owner {
			if has_belief(trigger_restriction_rule){
				return 0.0; //stops withdrawal completely
			}else if has_belief(trigger_attention_rule){
				return 0.5*myself.daily_withdrawal; //50% reduction
			}else{
				return myself.daily_withdrawal;
			}
		}
	}
}

species Farmer control: simple_bdi {
	Farmer farmer;
	int f_id;
	string profile;
	list<Pump> owned_pumps; // list of owned pumps 
	list<Farmer> my_group;
	int nb_pumps;
	string sub_basin; // sub-basin whose rules they will observe
	//int col_level; //column of the overall matrix with level series
	//list ref_level_list; //reference list that depends on the sub-basin
	float irrigation_area; //potential irrigation area [ha]
	float f_daily_withdrawal update: update_f_withdrawal();
	rgb color <- #grey;	int col_level;
	float yellow_level;
	float red_level;
	float current_level <- 1000 update:level_series[col_level,cycle];//level variation at the reference gauging station [cm] //might be given as an input of a hydrological model output
	bool aux_level_red <- false update:(current_level <= red_level);
	bool aux_level_yellow <- false update:(current_level <= yellow_level);
	bool aux_date_08 update:(current_date >= restriction_date);
	bool aux_date_07 update:(current_date >= attention_date);
	
	//action update_level (int cycle, string sub_basin){
		//}
	
	predicate trigger_attention_rule <- new_predicate("Attention rule must be obeyed");
	predicate trigger_restriction_rule <- new_predicate("Restriction rule must be obeyed");
	predicate obey_restriction_rule <- new_predicate("I am obeying the restriction rule");
	predicate obey_attention_rule <- new_predicate("I am obeying the restriction rule");
	
	/*aspect default {
		draw circle(150) color: color border: #black;
	}*/

	action update_f_withdrawal {
		return sum(collect(owned_pumps,each.daily_withdrawal));
	}
	
	reflex assign_beliefs {
		if(profile = "CP"){
			do remove_belief(trigger_restriction_rule);
			if((aux_date_08 = true) or (aux_level_red = true)){
				do add_belief(trigger_restriction_rule);
			}else if((aux_date_07 = true) or (aux_level_yellow = true)){
				do add_belief(trigger_attention_rule);
			}
		}else if (profile = 'CI'){
			if((aux_date_08 = true) and (aux_level_red = true)){
				do add_belief(trigger_restriction_rule);
			}else if((aux_date_07 = true) and (aux_level_yellow = true)){
				do add_belief(trigger_attention_rule);
			}
		}
	}
	
	rule belief: trigger_restriction_rule new_desire: obey_restriction_rule;
	rule belief: trigger_attention_rule new_desire: obey_attention_rule;	
}

// Auxiliar species for GUI experiments
species Land {
	aspect default {
		draw shape color: #darkgreen border: #black;
	}
}

species Channel {
	aspect default {
		draw shape color: #black border: #black;
	}
}

species Hidro {
	aspect default {
		draw shape color: #blue border: #black;
	}
}	

experiment teste_gui type: gui {
	output {
		/*display map refresh: every(1 #cycle) {
			species Hidro;
			species Channel;
			species Land;
			species Pump;
			species Farmer;
		}*/

		display Irrigation_per_pump refresh: every(1 #cycle) {
			chart "Individual water consumption (m³)" type: series x_serie_labels:my_day{
				datalist Pump collect (each.rotulo) value: Pump collect (each.daily_withdrawal) style: line ;
			}
		}

		display Irrigation_per_farmer refresh: every(1 #cycle) {
			chart "Total water consumption (m³)" type: series  x_serie_labels:my_day{
				datalist Farmer collect string(each.f_id) value: Farmer collect sum (each.owned_pumps collect each.daily_withdrawal) style: line;
			}
		}
		
		display Irrigation_total refresh: every(1 #cycle) {
			chart "Total water consumption (m³)" type: series x_serie_labels:my_day{
				data "All pumps" value: sum((Pump collect (each.daily_withdrawal))) style: line color: #black;
			}
		}

		display Irrigation_total_pump_profile refresh: every(1 #cycle) {
			chart "Water consumption (m³) per profile" type: series x_serie_labels:my_day{
				data "CP" value: sum((Pump where (each.f_profile = "CP")) collect (each.daily_withdrawal)) style: line color: #magenta;
				data "CI" value: sum((Pump where (each.f_profile = "CI")) collect (each.daily_withdrawal)) style: line color: #cyan;
				data "NC" value: sum((Pump where (each.f_profile = "NC")) collect (each.daily_withdrawal)) style: line color: #yellow;
			}
		}
		
		/*display AverageIrrigation_total_pump_profile refresh: every(1 #cycle) {
			chart "Average water consumption (m³) per pump per profile" type: series {
				data "CP" value: sum((Pump where (each.f_profile = "CP")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "CP")) color: #magenta;
				data "CI" value: sum((Pump where (each.f_profile = "CI")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "CI"))  color: #cyan;
				data "NC" value: sum((Pump where (each.f_profile = "NC")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "NC"))  color: #yellow;
			}
		}*/
	}
}

experiment repetitions type: batch repeat: 100 autorun: false keep_seed:true until: cycle = nb_days+1 { 	
	reflex end_of_runs {
		int sim <- 0;
		ask simulations { // at the end of the simulation, for each simulation
			sim <- sim + 1;	
		}
	}
} 