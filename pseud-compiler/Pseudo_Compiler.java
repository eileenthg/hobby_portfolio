import java.util.LinkedList;

public class Pseudo_Compiler {
	static String[] RESERVED_KEYWORDS = {"abstract",	"assert",	"boolean",	"break",	"byte",	"case","catch",	"char",	"class",	"const",	"continue",	"default", "double",	"do",	"else",	"enum",	"extends",	"false","final",	"finally",	"float",	"for",	"goto",	"if","implements",	"import",	"instanceof",	"int",	"interface",	"long", "native",	"new"}; 
	//not the complete list of reserved keywords
	public static void main(String[] args) {
		
		//warning, current implementation, input code MUST HAVE SPACE IN BETWEEN OPERATORS AND OPERANDS.
		//does not handle strings and parentheses and brackets.
		String inputCode = "int i; i = 0;";

		String[] codeLine = inputCode.split(";");
		
		LinkedList<Token> tokens = new LinkedList<Token>();
		
		for(String x: codeLine) {
			x = x.strip();
			
			//handle declarations
			//Would do this for every single primitive? Every single object???
			if(x.startsWith("int")) {
				//check whether same name already exists.
				//if does, raise error.
				if()
					tokens.add(new Token(x, "int"));
			}
				
			
			String[] operands = x.split("[*%=+-/^ ]");
			for(String y: operands) {
				y = y.strip();
				if (!isKeyword(y)) {
					
				}
				//System.out.println(y);
			}
			String[] operators = x.split("[a-z|A-Z|0-9]");
			for(String y: operators) {
				y = y.strip();
				
				//System.out.println(y);
			}
		}
			
	}
	
	static boolean isKeyword(String test){
		for(String x: RESERVED_KEYWORDS) {
			if(x.equals(test))
				return true;
		}
		return false;
	}
	
	static Token existingOperand(String test, LinkedList<Token>[] tokens) {
		ListIterator<Token> test = tokens.listIterator(0);
	}
}


class Token{
	String name;
	String value;
	
	Token(String name, String value){
		this.name = name;
		this.value = value;
	}
}