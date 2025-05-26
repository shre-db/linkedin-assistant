# Use the official Miniconda3 image from Docker Hub
FROM continuumio/miniconda3

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/conda/envs/linkedin-assistant/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH"

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Create the conda environment
RUN conda env create -f environment.yaml && \
    conda clean --all --yes

# Use bash and activate the env for subsequent commands
SHELL ["/bin/bash", "-c"]

# Optional but informative: show which environment will run by default
RUN echo "source activate linkedin-assistant" > ~/.bashrc

# Expose Streamlit's default port (only if you're using Streamlit)
EXPOSE 8501

# Correct CMD for running the app with environment activated
CMD ["conda", "run", "--no-capture-output", "-n", "linkedin-assistant", "python", "./app/main.py"]
