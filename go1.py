import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def main():
    st.title("부동산 상담 챗봇 🏠")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        try:
            model = initialize_gemini(api_key)
            
            # PDF 파일 업로드
            uploaded_file = st.file_uploader("부동산 관련 PDF 문서를 업로드하세요", type=['pdf'])
            
            if uploaded_file:
                pdf_text = extract_text_from_pdf(uploaded_file)
                st.success("PDF 파일이 성공적으로 업로드되었습니다!")
                
                # 사용자 질문 입력
                user_question = st.text_input("부동산에 관해 무엇이든 물어보세요:")
                
                if user_question:
                    # 프롬프트 구성
                    prompt = f"""
                    다음은 부동산 관련 문서의 내용입니다:
                    {pdf_text}
                    
                    사용자 질문: {user_question}
                    
                    위 문서의 내용을 참고하여 질문에 답변해주세요. 부동산 전문가처럼 친절하고 전문적으로 답변해주세요.
                    """
                    
                    with st.spinner('답변을 생성하고 있습니다...'):
                        response = model.generate_content(prompt)
                        st.write("🤖 챗봇 답변:")
                        st.write(response.text)
                        
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
            
if __name__ == "__main__":
    main()
